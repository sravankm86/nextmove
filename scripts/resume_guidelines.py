"""Standard frame for resume guidelines: validate values and render the document.

contracts/resume-guidelines-schema.json defines stable section and field IDs and types.
Values are {section_id: {field_id: value}} and live only in the user's private guidelines.
The same frame renders the public blank template, a private Google Doc (HTML) and, later,
a configurable UX. Usage:
  python scripts/resume_guidelines.py template            # rewrite templates/resume-guidelines.md
  python scripts/resume_guidelines.py html values.json    # print a filled HTML document
  python scripts/resume_guidelines.py check values.json   # validate values against the schema
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'contracts/resume-guidelines-schema.json'
TEMPLATE_PATH = ROOT / 'templates/resume-guidelines.md'


def load_schema():
    return json.loads(SCHEMA_PATH.read_text())


def _check(kind, value, spec, where, errors):
    if value is None or value == '' or value == []:
        return
    ok = {
        'text': lambda v: isinstance(v, str),
        'date': lambda v: isinstance(v, str) and len(v) == 10 and v[4] == '-' and v[7] == '-',
        'number': lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
        'boolean': lambda v: isinstance(v, bool),
        'list': lambda v: isinstance(v, list) and all(isinstance(x, str) for x in v),
        'range': lambda v: isinstance(v, dict) and set(v) == {'min', 'max'} and v['min'] <= v['max'],
        'select': lambda v: v in spec.get('options', []),
        'multi_select': lambda v: isinstance(v, list) and all(x in spec.get('options', []) for x in v),
        'table': lambda v: isinstance(v, list) and all(isinstance(r, dict) for r in v),
    }[kind](value)
    if not ok:
        errors.append('%s: invalid %s value' % (where, kind))
    elif kind == 'table':
        cols = {c['id']: c for c in spec['columns']}
        for i, row in enumerate(value):
            for key, cell in row.items():
                if key not in cols:
                    errors.append('%s[%d]: unknown column %s' % (where, i, key))
                else:
                    _check(cols[key]['type'], cell, cols[key], '%s[%d].%s' % (where, i, key), errors)


def validate(values, schema=None):
    """Return a list of problems; empty means every supplied value fits the frame."""
    schema = schema or load_schema()
    errors = []
    sections = {s['id']: s for s in schema['sections']}
    for sid, fields in (values or {}).items():
        if sid not in sections:
            errors.append('unknown section %s' % sid)
            continue
        specs = {f['id']: f for f in sections[sid]['fields']}
        for fid, value in fields.items():
            if fid not in specs:
                errors.append('%s.%s: unknown field' % (sid, fid))
            else:
                _check(specs[fid]['type'], value, specs[fid], '%s.%s' % (sid, fid), errors)
    consistency = (values or {}).get('company_consistency', {})
    if consistency.get('submitted_files_editable') is True:
        errors.append('company_consistency.submitted_files_editable must be false')
    return errors


def _fmt(kind, value, spec):
    if value is None or value == '' or value == []:
        return ''
    if kind == 'boolean':
        return 'Yes' if value else 'No'
    if kind in ('multi_select', 'list'):
        return '; '.join(value)
    if kind == 'range':
        return '%s to %s' % (value['min'], value['max'])
    return str(value)


def _type_label(spec):
    return spec['type'].replace('_', ' ')


def render_markdown(values=None, schema=None):
    """Blank (or filled) document in the standard frame."""
    schema = schema or load_schema()
    values = values or {}
    out = ['# Resume guidelines', '',
           'Standard frame `%s` v%d. Fill the Value column; keep section and field IDs unchanged. '
           'Options lists the allowed choices for select fields. Instructions holds natural-language '
           'guidance for the section; structured values take precedence. Facts always come from the '
           'registered master; this document decides selection, order, wording and layout.'
           % (schema['schema'], schema['version']), '']
    for n, s in enumerate(schema['sections'], 1):
        out += ['## %d. %s `%s`' % (n, s['title'], s['id']), '', s['purpose'], '',
                '| Field | ID | Type | Options | Value |', '|---|---|---|---|---|']
        tables, instructions = [], None
        for f in s['fields']:
            v = values.get(s['id'], {}).get(f['id'])
            if f['id'] == 'instructions':
                instructions = v
                continue
            if f['type'] == 'table':
                tables.append((f, v or []))
                out.append('| %s | `%s` | table | see below | |' % (f['label'], f['id']))
                continue
            opts = ' / '.join(f.get('options', []))
            out.append('| %s | `%s` | %s | %s | %s |' % (f['label'], f['id'], _type_label(f), opts,
                                                      _fmt(f['type'], v, f).replace('|', '/')))
        for f, rows in tables:
            cols = f['columns']
            out += ['', '**%s** `%s`: %s' % (f['label'], f['id'], f['help']), '',
                    '| ' + ' | '.join(c['id'] for c in cols) + ' |', '|' + '---|' * len(cols)]
            for row in rows or [{}]:
                out.append('| ' + ' | '.join(_fmt(c['type'], row.get(c['id']), c).replace('|', '/')
                                             for c in cols) + ' |')
        out += ['', '**Instructions:** ' + (instructions or '_(natural language, optional)_'), '']
    return '\n'.join(out).rstrip() + '\n'


def render_html(values, schema=None):
    """Filled document as HTML for Google Docs conversion (headings, tables, paragraphs)."""
    schema = schema or load_schema()
    e = lambda t: html.escape(str(t))
    doc = values.get('document', {})
    parts = ['<html><body><h1>Resume guidelines %s</h1>' % e(doc.get('version', '')),
             '<p>Standard frame <b>%s v%d</b>. Section and field IDs are stable; Value holds the setting; '
             'Instructions holds natural-language guidance, and structured values take precedence. '
             'Facts always come from the registered master.</p>' % (e(schema['schema']), schema['version'])]
    for n, s in enumerate(schema['sections'], 1):
        parts.append('<h2>%d. %s <code>[%s]</code></h2><p><i>%s</i></p>' % (n, e(s['title']), e(s['id']), e(s['purpose'])))
        rows, tables, instructions = [], [], None
        for f in s['fields']:
            v = values.get(s['id'], {}).get(f['id'])
            if f['id'] == 'instructions':
                instructions = v
            elif f['type'] == 'table':
                tables.append((f, v or []))
            else:
                opts = ' / '.join(f.get('options', []))
                rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><b>%s</b></td></tr>'
                            % (e(f['label']), e(f['id']), e(_type_label(f)), e(opts), e(_fmt(f['type'], v, f))))
        if rows:
            parts.append('<table border="1"><tr><th>Field</th><th>ID</th><th>Type</th><th>Options</th><th>Value</th></tr>%s</table>' % ''.join(rows))
        for f, data in tables:
            cols = f['columns']
            head = ''.join('<th>%s</th>' % e(c['id']) for c in cols)
            body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % e(_fmt(c['type'], r.get(c['id']), c)) for c in cols) for r in data)
            parts.append('<p><b>%s</b> [%s]: %s</p><table border="1"><tr>%s</tr>%s</table>' % (e(f['label']), e(f['id']), e(f['help']), head, body))
        parts.append('<p><b>Instructions:</b> %s</p>' % e(instructions or '(none)'))
    parts.append('</body></html>')
    return ''.join(parts)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'template'
    if cmd == 'template':
        TEMPLATE_PATH.write_text(render_markdown())
    else:
        vals = json.loads(Path(sys.argv[2]).read_text())
        problems = validate(vals)
        if problems:
            print('\n'.join(problems), file=sys.stderr)
            raise SystemExit(1)
        print(render_html(vals) if cmd == 'html' else 'Values fit the frame.')
