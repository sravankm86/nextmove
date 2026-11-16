import copy
import re
import sys
import unittest
import tempfile
import hashlib
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from role_gate import career_rating, resume_rating, scored_review, review_frame_contract
from stage_state import run_duplicate_match, review_ready


def finding(status, **extra):
    return {'status':status,'evidence':'Verified source' if status!='unknown' else None,**extra}


class ReviewFrameTests(unittest.TestCase):
    def test_published_tables_match_the_machine_contract(self):
        _,contract=review_frame_contract()
        text=(Path(__file__).resolve().parents[1]/'stages/review.md').read_text()
        sections=[text.split('## Step 2.')[1].split('## Step 3.')[0],text.split('## Step 3.')[1]]
        for axis,section in zip(['career','resume'],sections):
            values={label:int(score) for label,score in re.findall(r'\| (Low|Medium|High) \|[^\n|]+\| (\d+) \|',section)}
            self.assertEqual(values,contract[axis])

    def test_career_objective_failure_differs_from_soft_preference(self):
        self.assertEqual(career_rating([finding('not_met',objective=True)]),'Low')
        self.assertEqual(career_rating([finding('met'),finding('not_met',objective=False)]),'Medium')
        self.assertEqual(career_rating([finding('met'),finding('met')]),'High')
        self.assertEqual(career_rating([finding('unknown',objective=True)]),'Unresolved')

    def test_resume_uses_all_preferred_not_majority(self):
        self.assertEqual(resume_rating([finding('met')],[finding('met'),finding('met'),finding('not_met')]),'Medium')
        self.assertEqual(resume_rating([finding('met')],[finding('met')]),'High')
        self.assertEqual(resume_rating([finding('not_met')],[finding('met')]),'Low')
        self.assertEqual(resume_rating([finding('unknown')],[finding('met')]),'Unresolved')
        self.assertEqual(resume_rating([finding('met')],[finding('unknown')]),'Unresolved')
        self.assertEqual(resume_rating([finding('met')],[],preferred_listed=False),'High')
        self.assertEqual(resume_rating([],[],preferred_listed=True),'Unresolved')

    def test_all_nine_current_score_combinations_and_unknown(self):
        _,contract=review_frame_contract()
        self.assertEqual(contract['career'],{'Low':0,'Medium':2,'High':3})
        self.assertEqual(contract['resume'],{'Low':1,'Medium':2,'High':3})
        expected=[['Not pursuing','Not pursuing','Not pursuing'],['Not pursuing','Need review','Queued'],['Need review','Queued','Queued']]
        for ci,c in enumerate(['Low','Medium','High']):
            for ri,r in enumerate(['Low','Medium','High']):
                self.assertEqual(scored_review(c,r,contract=contract)['outcome'],expected[ci][ri])
        self.assertEqual(scored_review('High','Unresolved',contract=contract)['outcome'],'Need review')
        self.assertEqual(scored_review('High','Low',minimum_failure=True,contract=contract)['outcome'],'Need review')

    def test_impossible_resume_bounds_stop_but_unknown_career_always_waits(self):
        for resume in ['Low','Medium','High','Unresolved']:
            self.assertEqual(scored_review('Low',resume)['outcome'],'Not pursuing')
            self.assertEqual(scored_review('Unresolved',resume)['outcome'],'Need review')
        result=scored_review('Low','Unresolved')
        self.assertIsNone(result['resume_score'])
        self.assertIsNone(result['total'])
        self.assertEqual(scored_review('Medium','Unresolved')['outcome'],'Need review')
        self.assertEqual(scored_review('High','Unresolved')['outcome'],'Need review')

    def test_review_file_alone_changes_scores_and_automatic_identity(self):
        source=Path(__file__).resolve().parents[1]/'stages/review.md'
        original,contract=review_frame_contract()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'review.md'
            text=source.read_text().replace('Total 5–6','Total 4–6').replace('Total 4 |','Total 3 |').replace('Total 0–3','Total 0–2')
            path.write_text(text)
            identity,changed=review_frame_contract(path)
            self.assertNotEqual(identity,original)
            self.assertEqual(identity,'review-sha256:'+hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(scored_review('High','Low',contract=changed)['outcome'],'Queued')
            path.write_text(text.replace('Total 4–6','Total 5–6'))
            with self.assertRaises(ValueError):review_frame_contract(path)

    def test_invalid_or_unsupported_claims_do_not_become_scores(self):
        with self.assertRaises(ValueError):career_rating([{'status':'met'}])
        with self.assertRaises(ValueError):scored_review('Strong','High')

    def test_run_identity_uses_specific_links_and_verified_ids(self):
        a={'company_id':'company','role_name':'Senior PM','posted_date':'2026-01-01','job_url':'https://jobs.example.test/roles/one?utm_source=x','job_url_verified_specific':True}
        b={**a,'job_url':'https://jobs.example.test/roles/one'}
        self.assertEqual(run_duplicate_match(a,b)['decision'],'duplicate')
        self.assertEqual(run_duplicate_match(a,{**b,'company_id':'other'})['decision'],'distinct')
        self.assertEqual(run_duplicate_match({**a,'job_url_verified_specific':False},{**b,'job_url_verified_specific':False})['decision'],'unresolved')
        self.assertEqual(run_duplicate_match({**a,'role_id':'a','role_id_verified':True},{**b,'role_id':'b','role_id_verified':True})['decision'],'unresolved')
        self.assertEqual(run_duplicate_match({**a,'role_id':'a','role_id_verified':True},{**b,'role_id':'a','role_id_verified':True})['decision'],'duplicate')

    def test_new_acceptance_requires_current_scoring_and_run_identity(self):
        policy,contract=review_frame_contract();c=max(contract['career'],key=contract['career'].get);r=max(contract['resume'],key=contract['resume'].get)
        inputs={'goals':'g','master':'m','policy':policy,'eligibility_policy':'e','jd_hash':'jd'}
        run={'id':'run','Input versions (JSON)':{'stage_inputs':{'review':inputs}}}
        app={'id':'job','Lifecycle status':'Queued','Role eligibility':'Eligible','Career fit':c,'Resume fit':r,'Review run':['run']}
        state={'record_id':'job','stage_runs':{'review':'run'},'run_checks':{'duplicate':{'status':'unique','checked_in_run':'run','evidence':'Verified posting identity'}},'review':{'assessment_method':contract['assessment_method'],'scoring':scored_review(c,r),'decision':'approve','assessment_complete':True,'jd_hash':'jd','current_description':True,'evidence':'Verified indexed assessment'}}
        self.assertTrue(review_ready(app,state,[run],inputs))
        for key in ['scoring','evidence','assessment_method']:
            changed=copy.deepcopy(state);changed['review'].pop(key)
            self.assertFalse(review_ready(app,changed,[run],inputs))
        changed=copy.deepcopy(state);changed['run_checks']['duplicate']['status']='unresolved'
        self.assertFalse(review_ready(app,changed,[run],inputs))
        self.assertFalse(review_ready(app,state,[run],{**inputs,'policy':'changed'}))


if __name__=='__main__':unittest.main()
