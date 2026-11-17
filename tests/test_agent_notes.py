import re, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from stage_state import agent_note_problems


def documented_examples():
    text = (ROOT / 'DATA.md').read_text()
    section = text.split('## Writing Agent notes', 1)[1].split('\n## ', 1)[0]
    return re.findall(r'^\| [A-Z][a-z]+(?: [a-z]+)? \| (.+) \|$', section, re.M)


class AgentNoteTests(unittest.TestCase):
    def test_documented_examples_pass(self):
        examples = documented_examples()
        self.assertGreaterEqual(len(examples), 8)
        for note in examples:
            with self.subTest(note=note):
                self.assertEqual(agent_note_problems(note), [])

    def test_quoted_question_does_not_count_as_a_sentence_break(self):
        note = 'Waiting for your answer: the form asks "Are you willing to relocate?" and the answer bank has no answer. Add it and this role will continue.'
        self.assertEqual(agent_note_problems(note), [])

    def test_old_terse_or_code_like_notes_are_flagged(self):
        cases = {
            '': 'empty',
            'Review: High+Medium; jd_hash changed. Next: rerun review_ready.': 'snake_case field or code name',
            'Scored 3 + 2 = 5 so Queued.': 'score arithmetic',
            'Linked to recAbCdEfGhIjKlMn for detail.': 'record or field ID',
            'Resume verified: 259a9681bc1f71959fbc7562f00eb277.': 'hash',
            'Held. {"window": 30}': 'JSON or braces',
            'One. Two. Three. Four.': 'more than three sentences',
            ' '.join(['word'] * 70) + '.': 'longer than about 60 words',
        }
        for note, problem in cases.items():
            with self.subTest(note=note):
                self.assertIn(problem, agent_note_problems(note))


if __name__ == '__main__':
    unittest.main()
