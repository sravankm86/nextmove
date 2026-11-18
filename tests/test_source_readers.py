import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import artifact_reader as a
import source_registry as s


class SourceTests(unittest.TestCase):
    def test_document_hash_uses_all_tab_body_text_without_style_metadata(self):
        run = lambda text: {'paragraph': {'elements': [{'textRun': {'content': text}}]}}
        doc = {'tabs': [{'documentTab': {'body': {'content': [run('One\n')]}},
                         'childTabs': [{'body': {'content': [run('Two\n')]}}]},
                        {'body': {'content': [{'table': {'tableRows': [{'tableCells': [
                            {'content': [run('Three\n')]}]}]}}]}}]}
        self.assertEqual(s.document_text(doc), 'One\nTwo\nThree\n')

    def test_exact_job_selection_excludes_old_decisions_and_shared_inputs(self):
        text = 'Full qualifications and preferred experience'
        document = {'goals': 'private shared data', 'records': [
            {'record_id': 'one', 'status': 'Old result', 'source': {'description': text,
             'description_sha256': hashlib.sha256(text.encode()).hexdigest()}},
            {'record_id': 'two', 'source': {'description': 'Other role'}}]}
        result = a.select(document, 'job', 'one')
        self.assertEqual(result['description'], text)
        self.assertNotIn('status', result)
        self.assertNotIn('goals', result)
        with self.assertRaises(ValueError): a.select(document, 'job', 'unknown')
        with self.assertRaises(ValueError): a.select({'records': document['records'] * 2}, 'job', 'one')

    def test_missing_description_or_changed_bytes_blocks(self):
        for source in [{}, {'description': 'Changed', 'description_sha256': 'incorrect'}]:
            with self.assertRaises(ValueError):
                a.select({'records': [{'record_id': 'one', 'source': source}]}, 'job', 'one')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'input.json'
            path.write_text(json.dumps({'rows': [{'company_id': 'one', 'fact': 'evidence'}]}))
            self.assertEqual(a.read(path, 'company', 'one')['record']['fact'], 'evidence')
            with self.assertRaises(ValueError): a.read(path, 'company', 'one', 'wrong')

    def test_other_artifact_identities(self):
        for kind, (collection, key) in a.SELECTORS.items():
            if kind != 'job':
                self.assertEqual(a.select({collection: [{key: 'exact'}]}, kind, 'exact')[key], 'exact')

    def test_registry_and_extraction_versions_are_independent(self):
        source = {'file_id': 'source-one', 'revision': 'new', 'text_sha256': s.text_hash('new')}
        self.assertEqual(s.inspect(source, source)['state'], 'Current')
        self.assertEqual(s.inspect(source | {'revision': 'old'}, source)['state'], 'Changed')
        self.assertFalse(s.cache_current({'source_revision': 'old'}, source))
        self.assertTrue(s.cache_current({'source_revision': 'new', 'source_text_sha256': source['text_sha256']}, source))
        self.assertFalse(s.cache_current({'source_revision': 'new', 'source_text_sha256': source['text_sha256'], 'cache_stale': True}, source))
        self.assertFalse(s.inspect(source | {'use': 'historical_only'}, source)['usable_as_current'])
        with self.assertRaises(ValueError): s.inspect(source, source | {'file_id': 'other'})


if __name__ == '__main__': unittest.main()
