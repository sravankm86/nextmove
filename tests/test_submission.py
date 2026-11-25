"""Guard rails for the explicit-only Submit stage."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from stage_state import application_write
from submission import (ATTEMPT_SCHEMA, manifest, policy, prior_attempt_uncertain, proof_verified,
                        same_site, submission_eligible, submission_result)

FORM = 'https://jobs.example.test/acme/123/apply'


def attempt(**over):
    base = {'schema': ATTEMPT_SCHEMA, 'attempt_key': 'acme-123-1', 'started_at': '2026-01-01T12:00:00Z',
            'form_url': FORM, 'manifest_sha256': 'abc', 'submit_clicked': True,
            'proof': {'page_url': 'https://jobs.example.test/acme/123/thanks', 'confirmation_text': 'Thanks, we received your application.',
                      'file_id': 'drive-file', 'sha256': 'proof-hash', 'observed_at': '2026-01-01T12:01:00Z', 'verified': True}}
    base.update(over)
    return base


class PolicyTests(unittest.TestCase):
    def test_disabled_unless_explicitly_enabled(self):
        self.assertFalse(policy(None)['enabled'])
        self.assertFalse(policy({'enabled': 'yes'})['enabled'])
        self.assertTrue(policy({'enabled': True})['enabled'])
        self.assertEqual(policy({'max_per_run': -1})['max_per_run'], 10)
        self.assertEqual(policy({'max_per_company_per_day': 0})['max_per_company_per_day'], 0)


class EligibilityTests(unittest.TestCase):
    app = {'id': 'role', 'Job key': 'acme:123', 'Lifecycle status': 'Ready'}

    def test_only_live_ready_roles_with_passing_checks(self):
        self.assertTrue(submission_eligible(self.app, {}, ready=True))
        self.assertFalse(submission_eligible(self.app, {}, ready=False))
        for status in ['Queued', 'Needs answer', 'Apply manually', 'Applied', 'Interviewing']:
            self.assertFalse(submission_eligible({**self.app, 'Lifecycle status': status}, {}, ready=True))
        self.assertFalse(submission_eligible({**self.app, 'Submission attempt key': 'legacy'}, {}, ready=True))

    def test_possible_earlier_submission_blocks_automatic_retry(self):
        clean = {'submit': {'attempts': [attempt(submit_clicked=False, proof=None)]}}
        self.assertFalse(prior_attempt_uncertain(clean))
        self.assertTrue(submission_eligible(self.app, clean, ready=True))
        for clicked in [True, None]:
            state = {'submit': {'attempts': [attempt(submit_clicked=clicked, proof=None)]}}
            self.assertTrue(prior_attempt_uncertain(state))
            self.assertFalse(submission_eligible(self.app, state, ready=True))
            self.assertFalse(submission_eligible(self.app, state, ready=True, human_request={'quote': ' '}))
            self.assertTrue(submission_eligible(self.app, state, ready=True,
                                                human_request={'quote': 'Retry Acme, I checked it was not received', 'observed_at': 'now'}))


class ManifestTests(unittest.TestCase):
    app = {'id': 'role', 'Job key': 'acme:123'}

    def inspection(self, *questions):
        return {'form_url': FORM, 'form_hash': 'form', 'questions': list(questions)}

    def test_only_approved_values_and_files(self):
        q = {'field_key': 'name', 'required': True, 'sensitive': False,
             'answer': {'mapped_answer': 'Example Person', 'mapping_verified': True}}
        optional = {'field_key': 'hobby', 'required': False, 'sensitive': False}
        result = manifest(self.app, self.inspection(q, optional), 'resume-hash')
        self.assertEqual(result['fields'], [{'field_key': 'name', 'value': 'Example Person'}])
        self.assertEqual(manifest(self.app, self.inspection(q, optional), 'resume-hash')['sha256'], result['sha256'])
        self.assertNotEqual(manifest(self.app, self.inspection(q), 'other-resume')['sha256'], result['sha256'])
        for bad in [{'field_key': 'eeo', 'required': False, 'sensitive': True},
                    {'field_key': 'why', 'required': True, 'sensitive': False, 'answer': {'mapped_answer': 'x', 'mapping_verified': False}}]:
            with self.assertRaises(ValueError):
                manifest(self.app, self.inspection(q, bad), 'resume-hash')
        with self.assertRaises(ValueError):
            manifest(self.app, self.inspection(q), 'resume-hash', [{'field_key': 'cover', 'sha256': 'c', 'approved': False}])
        with self.assertRaises(ValueError):
            manifest(self.app, self.inspection(q), '')
        cover = manifest(self.app, self.inspection(q), 'resume-hash', [{'field_key': 'cover', 'sha256': 'c', 'approved': True, 'kind': 'cover_letter'}])
        self.assertEqual(cover['files'][-1], {'kind': 'cover_letter', 'field_key': 'cover', 'sha256': 'c'})


class ProofTests(unittest.TestCase):
    def test_applied_needs_verified_confirmation_on_the_same_site(self):
        self.assertTrue(proof_verified(attempt()))
        self.assertEqual(submission_result(attempt()), {'status': 'Applied'})
        for change in [{'submit_clicked': False}, {'proof': None}, {'schema': 'old'}, {'manifest_sha256': ''}]:
            self.assertFalse(proof_verified(attempt(**change)))
        for key, value in [('page_url', 'https://evil.example.org/thanks'), ('page_url', 'http://jobs.example.test/thanks'),
                           ('confirmation_text', ' '), ('verified', False), ('file_id', '')]:
            a = attempt(); a['proof'] = {**a['proof'], key: value}
            self.assertFalse(proof_verified(a))

    def test_failures_end_at_apply_manually_with_a_warning_when_possibly_submitted(self):
        before = submission_result(attempt(submit_clicked=False, proof=None, blocker={'kind': 'sign_in_required', 'detail': 'Login page'}))
        self.assertEqual(before, {'status': 'Apply manually', 'kind': 'sign_in_required', 'detail': 'Login page', 'possibly_submitted': False})
        after = submission_result(attempt(proof=None))
        self.assertEqual((after['status'], after['kind'], after['possibly_submitted']), ('Apply manually', 'no_confirmation', True))
        self.assertTrue(submission_result({'submit_clicked': None})['possibly_submitted'])
        self.assertEqual(submission_result({'submit_clicked': False, 'blocker': {'kind': 'made_up'}})['kind'], 'no_confirmation')

    def test_same_site(self):
        self.assertTrue(same_site('https://apply.example.test/x', 'https://jobs.example.test/y'))
        self.assertFalse(same_site('https://example.test.evil.org/x', 'https://jobs.example.test/y'))
        self.assertFalse(same_site('', FORM))


class WriteGuardTests(unittest.TestCase):
    def test_applied_requires_ready_and_verified_proof(self):
        ready = {'Lifecycle status': 'Ready'}
        good = {'submit': {'attempts': [attempt()]}}
        self.assertEqual(application_write({'Lifecycle status': 'Applied'}, existing_application=ready, existing_state=good),
                         {'Lifecycle status': 'Applied'})
        for app, state in [(ready, {}), (ready, {'submit': {'attempts': [attempt(proof=None)]}}),
                           ({'Lifecycle status': 'Queued'}, good)]:
            with self.assertRaises(ValueError):
                application_write({'Lifecycle status': 'Applied'}, existing_application=app, existing_state=state)
        with self.assertRaises(ValueError):
            application_write({'Agent notes': 'edit'}, existing_application={'Lifecycle status': 'Applied'})


if __name__ == '__main__':
    unittest.main()
