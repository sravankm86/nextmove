import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from resume_guidelines import load_schema, render_html, render_markdown, validate


class ResumeGuidelinesFrameTests(unittest.TestCase):
    def test_every_section_has_typed_fields_and_instructions(self):
        schema = load_schema()
        types = set(schema['field_types'])
        for section in schema['sections']:
            self.assertEqual(section['fields'][-1]['id'], 'instructions')
            for field in section['fields']:
                self.assertIn(field['type'], types)
                if field['type'] in ('select', 'multi_select'):
                    self.assertTrue(field['options'])

    def test_valid_values_pass_and_render(self):
        values = {'document': {'version': 'v01', 'status': 'Approved', 'effective_date': '2026-01-01'},
                  'company_consistency': {'window_days': 30, 'within_window': 'Reuse the exact submitted version',
                                          'submitted_files_editable': False},
                  'layout': {'font_size_pt': {'min': 10, 'max': 11}, 'fonts': ['Arial']},
                  'bases': {'catalogue': [{'base_id': 'platform', 'default_pages': 2, 'status': 'Approved'}]}}
        self.assertEqual(validate(values), [])
        self.assertIn('platform', render_html(values))
        self.assertIn('| Window (days) | `window_days` | number |  | 30 |', render_markdown(values))

    def test_invalid_values_are_reported_not_guessed(self):
        bad = {'document': {'status': 'Final'}, 'layout': {'fonts': ['Comic Sans'], 'font_size_pt': {'min': 12, 'max': 10}},
               'company_consistency': {'submitted_files_editable': True, 'window_days': 'thirty'},
               'bases': {'catalogue': [{'base_id': 'x', 'colour': 'blue'}]}, 'unknown': {}}
        problems = validate(bad)
        for fragment in ['document.status', 'layout.fonts', 'layout.font_size_pt', 'window_days',
                         'submitted_files_editable must be false', 'unknown column colour', 'unknown section unknown']:
            self.assertTrue(any(fragment in p for p in problems), fragment)


if __name__ == '__main__':
    unittest.main()
