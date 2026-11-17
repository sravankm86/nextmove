import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_repo import PRIVATE_IDS, ROLE_WORDS, personal_content_issues


class PublicRepoTests(unittest.TestCase):
    def test_repository_has_no_personal_settings_or_private_ids(self):
        self.assertEqual(personal_content_issues(ROOT), [])

    def test_guard_patterns_catch_personal_content(self):
        self.assertTrue(ROLE_WORDS.search('Scan for senior Product Manager roles'))
        self.assertTrue(ROLE_WORDS.search('propose Series C+ companies'))
        self.assertFalse(ROLE_WORDS.search('Funding stages run to Series E+ and Public'))
        # Samples are assembled at run time so this file itself stays clean.
        ids = ['app' + 'AbCdEfGhIjKlMn', 'https://drive.google.com/file/d/' + '1abcdefghijklmnopqrstuvwxyz/view', 'someone' + '@' + 'gmail.com']
        for sample, (pattern, _) in zip(ids, PRIVATE_IDS):
            self.assertTrue(pattern.search(sample))
        self.assertFalse(PRIVATE_IDS[2][0].search('alex' + '@' + 'example.com'))


if __name__ == '__main__':
    unittest.main()
