"""Select verified records from a downloaded private artifact without dumping the bundle.

The harness downloads through its own connector; this module has no network or credentials.
"""
import argparse
import hashlib
import json
from pathlib import Path

SELECTORS = {'job': ('records', 'record_id'), 'company': ('rows', 'company_id'),
             'source': ('sources', 'source_id')}


def select(document, kind, identity):
    if kind not in SELECTORS or not identity:
        raise ValueError('Known artifact kind and exact identity required')
    collection, key = SELECTORS[kind]
    records = document.get(collection)
    if not isinstance(records, list):
        raise ValueError('Unsupported artifact shape: ' + collection)
    matches = [r for r in records if isinstance(r, dict) and r.get(key) == identity]
    if len(matches) != 1:
        raise ValueError('Expected exactly one matching record; found ' + str(len(matches)))
    record = matches[0]
    if kind == 'job':
        source = record.get('source') or {}
        text = source.get('description')
        if not isinstance(text, str) or not text.strip():
            raise ValueError('Selected record has no full job description')
        actual = hashlib.sha256(text.encode()).hexdigest()
        if source.get('description_sha256') and source['description_sha256'] != actual:
            raise ValueError('Job description content hash mismatch')
        return {'record_id': identity, 'company': record.get('company'), 'role': record.get('role'),
                'description': text, 'description_sha256': actual,
                'url': source.get('url'), 'job_key': source.get('job_key')}
    return record


def read(path, kind, identity, expected_sha256=None):
    raw = Path(path).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if expected_sha256 and actual != expected_sha256:
        raise ValueError('Artifact content hash mismatch')
    return {'artifact_sha256': actual, 'record': select(json.loads(raw), kind, identity)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--kind', required=True, choices=SELECTORS)
    parser.add_argument('--id', required=True)
    parser.add_argument('--sha256')
    args = parser.parse_args()
    print(json.dumps(read(args.path, args.kind, args.id, args.sha256), ensure_ascii=False))


if __name__ == '__main__':
    main()
