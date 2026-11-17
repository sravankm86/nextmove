import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_eval import outcome, score


class ReviewEvalTest(unittest.TestCase):
    def test_outcomes(self):
        self.assertEqual(outcome('Pursue', 'Queued'), 'agree')
        self.assertEqual(outcome('Not pursuing', 'Not pursuing'), 'agree')
        self.assertEqual(outcome('Not pursuing', 'Queued'), 'false_queue')
        self.assertEqual(outcome('Pursue', 'Not pursuing'), 'missed')
        self.assertEqual(outcome('Pursue', 'Need review'), 'deferred')
        with self.assertRaises(ValueError):
            outcome('Maybe', 'Queued')

    def test_score_filters_inactive_and_split(self):
        rows = [
            {'verdict': 'Pursue', 'prediction': 'Queued', 'split': 'Train'},
            {'verdict': 'Not pursuing', 'prediction': 'Queued', 'split': 'Holdout'},
            {'verdict': 'Pursue', 'prediction': 'Need review', 'split': 'Train', 'active': False},
        ]
        self.assertEqual(score(rows)['status_match'], 0.5)
        self.assertEqual(score(rows, 'Holdout')['false_queue'], 1)
        self.assertIsNone(score([])['status_match'])

class ReplayIntegrityTest(unittest.TestCase):
    def dataset(self):
        from review_eval import digest
        root = Path(__file__).resolve().parents[1]
        source = lambda text: {'text': text, 'sha256': digest(text), 'identity': 'frozen-example'}
        return {'context': {'goals': source('Enterprise PM roles'), 'master': source('Demonstrated PM facts'),
                            'confirmed_facts': source('No invented experience'),
                            'instructions': source((root / 'stages/review.md').read_text())},
                'cases': [{'case_id': 'opaque-example', 'entity_id': 'example-role', 'verdict': 'Pursue',
                           'reason': 'ANSWER-SECRET', 'split': 'Holdout', 'active': True,
                           'inputs': {'role': 'Senior PM', 'jd_text': 'Full exact JD',
                                      'jd_sha256': digest('Full exact JD'),
                                      'company': {'name': 'Example', 'search_status': 'Allow',
                                                  'evidence_identity': 'company-version',
                                                  'Agent notes': 'PRIOR-PREDICTION-SECRET'}}}]}

    def prediction(self, bundle):
        return {'bundle_sha256': bundle['bundle_sha256'], 'predictions': [
            {'case_id': 'opaque-example', 'career_fit': 'High', 'resume_fit': 'High',
             'status': 'Queued', 'reason': 'Critical asks are supported by the frozen evidence.'}]}

    def test_labels_and_prior_outputs_never_enter_reviewer_bundle(self):
        import json
        from review_eval import prepare
        bundle, key = prepare(self.dataset())
        raw = json.dumps(bundle)
        for secret in ['ANSWER-SECRET', 'PRIOR-PREDICTION-SECRET', 'Holdout', 'verdict']:
            self.assertNotIn(secret, raw)
        self.assertEqual(key['cases'][0]['verdict'], 'Pursue')

    def test_feedback_clears_only_after_verified_capture_and_exact_reread(self):
        from review_eval import feedback_id, feedback_action, may_clear
        note = 'Pursue: strong match.'
        fid = feedback_id('Review', 'example-role', note)
        receipt = {'feedback_id': fid, 'case_id': 'case', 'snapshot_ref': 'snapshot', 'history_id': 'event',
                   'eval_verified': True, 'snapshot_verified': True, 'history_verified': True}
        self.assertTrue(may_clear('Review', 'example-role', note, note, receipt))
        self.assertFalse(may_clear('Review', 'example-role', note, note + ' Human edit.', receipt))
        self.assertFalse(may_clear('Review', 'example-role', note, note, {**receipt, 'eval_verified': False}))
        self.assertEqual(feedback_action('Review', 'example-role', note, [{'feedback_id': fid, 'case_id': 'case'}])['action'], 'reuse')
        self.assertNotEqual(fid, feedback_id('Review', 'another-role', note))

    def test_unknown_duplicate_or_wrong_input_predictions_fail(self):
        import copy
        from review_eval import prepare, evaluate
        bundle, key = prepare(self.dataset());p = self.prediction(bundle)
        self.assertEqual(evaluate(bundle, key, p)['overall']['positive_recall'], 1)
        bad = copy.deepcopy(p);bad['predictions'] *= 2
        with self.assertRaises(ValueError): evaluate(bundle, key, bad)
        bad = copy.deepcopy(p);bad['bundle_sha256'] = 'other-inputs'
        with self.assertRaises(ValueError): evaluate(bundle, key, bad)
        bad = copy.deepcopy(p);bad['predictions'][0]['status'] = 'Not pursuing'
        with self.assertRaises(ValueError): evaluate(bundle, key, bad)

    def test_missing_jd_is_unscored_not_an_automatic_rejection(self):
        from review_eval import prepare, evaluate
        d = self.dataset();d['cases'][0]['inputs']['jd_text'] = ''
        bundle, key = prepare(d)
        report = evaluate(bundle, key, {'bundle_sha256': bundle['bundle_sha256'], 'predictions': []})
        self.assertFalse(report['complete']);self.assertEqual(report['overall']['unscored'], 1)
        self.assertEqual(report['overall']['positive_recall'], 0)

    def test_instruction_candidate_comparison_keeps_facts_fixed(self):
        from review_eval import prepare, evaluate, compare, digest
        d = self.dataset();bundle, key = prepare(d);baseline = evaluate(bundle, key, self.prediction(bundle))
        d['context']['instructions']['text'] += '\nClarify evidence without changing score rules.\n'
        d['context']['instructions']['sha256'] = digest(d['context']['instructions']['text'])
        b2, k2 = prepare(d);candidate = evaluate(b2, k2, self.prediction(b2))
        self.assertEqual(compare(baseline, candidate)['regressed'], [])
        d['context']['master']['text'] += ' Different candidate fact.'
        d['context']['master']['sha256'] = digest(d['context']['master']['text'])
        b3, k3 = prepare(d)
        with self.assertRaises(ValueError): compare(baseline, evaluate(b3, k3, self.prediction(b3)))

    def test_frozen_files_cannot_be_overwritten(self):
        import tempfile
        from review_eval import write_new
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            write_new(path, {'version': 1})
            write_new(path, {'version': 1})
            with self.assertRaises(FileExistsError): write_new(path, {'version': 2})
            with self.assertRaises(ValueError): write_new(path, {'version': 1}, [path])


if __name__ == '__main__':
    unittest.main()
