import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lifecycle import STATUSES, END_STATES, LEGACY_READ_ONLY, PREPARE_INPUTS, PROTECTED_OUTCOMES, SUBMIT_INPUTS
from stage_state import application_write, protected_history, merge_state

class LifecycleTests(unittest.TestCase):
    def test_nine_active_states_and_stage_exits(self):
        self.assertEqual(STATUSES,['Inventoried','Need review','Queued','Ready','Needs answer','Apply manually','Applied','Not pursuing','Duplicate'])
        self.assertEqual(END_STATES,{'Ready','Apply manually','Applied','Not pursuing','Duplicate'})
        self.assertEqual(SUBMIT_INPUTS,{'Ready'})
        self.assertEqual(PREPARE_INPUTS,{'Queued','Needs answer'})
        self.assertNotIn('Needs answer',LEGACY_READ_ONLY)
        self.assertEqual(application_write({'Lifecycle status':'Ready'},existing_application={'Lifecycle status':'Needs answer'}),{'Lifecycle status':'Ready'})
        commands=json.loads((ROOT/'contracts/commands.json').read_text())
        self.assertEqual(commands['pipeline'],['Curate','Scan','Review','Prepare'])
        self.assertEqual(commands['endpoint'],'Ready')
        self.assertFalse({'Apply','Track'} & {c['command'] for c in commands['commands']})
        submit=next(c for c in commands['commands'] if c['command']=='Submit')
        self.assertTrue(submit['explicit_only']);self.assertFalse(submit['included_in_run'])
        self.assertNotIn('Submit',commands['pipeline'])

    def test_historical_outcomes_and_attempts_cannot_be_reopened(self):
        histories=[{'Lifecycle status':s} for s in PROTECTED_OUTCOMES]
        histories.append({'Lifecycle status':'Queued','Submission attempt key':'legacy'})
        for old in histories:
            self.assertTrue(protected_history(old))
            with self.assertRaises(ValueError):application_write({'Lifecycle status':'Queued'},existing_application=old)
            self.assertEqual(application_write({'Feedback':None},existing_application=old),{'Feedback':None})
        with self.assertRaises(ValueError):
            application_write({'Agent notes':'Reopening'},existing_application={'Lifecycle status':'Queued'},existing_state={'submission':{'attempt_key':'legacy'}})
        for old in ['Confirmed','Needs review','Offer','Submission uncertain',*LEGACY_READ_ONLY]:
            with self.assertRaises(ValueError):application_write({'Lifecycle status':old})
        for old in ['Applied']:
            with self.assertRaises(ValueError):application_write({'Lifecycle status':old})
        for field in ['Submission run','Submission attempt key','Applied on','Confirmation reference']:
            with self.assertRaises(ValueError):application_write({field:'old'})

    def test_active_answer_links_are_permitted(self):
        self.assertEqual(application_write({'Application questions':['question-one']}), {'Application questions':['question-one']})

    def test_active_state_merge_preserves_opaque_legacy_history(self):
        old={'schema':'nextmove.evidence.v1','record_id':'role','submission':{'attempt_key':'legacy'}}
        merged=merge_state(old,record_id='role',job_key='employer:role',stage='scan',values={'observed':True})
        self.assertEqual(merged['submission'],old['submission'])
        with self.assertRaises(ValueError):merge_state(old,record_id='role',job_key='employer:role',stage='submission',values={})
        with self.assertRaises(ValueError):merge_state(old,record_id='other',job_key='employer:role',stage='scan',values={})

if __name__=='__main__':unittest.main()
