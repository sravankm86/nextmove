"""Repeatable readers for official Greenhouse, Ashby and Lever catalogs.

Enumeration is transient: this script never writes Airtable or filters candidates.
Other providers need their own validated reader; no fallback implies coverage.
"""
import argparse
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

VERSION = 'official-json-v1'


def enumerate_catalog(kind, fetch):
    """Fetch(offset) returns a decoded official response. End proof is provider-specific."""
    if kind not in {'greenhouse', 'ashby', 'lever'}:
        raise ValueError('Unsupported provider')
    jobs, seen, pages, offset = [], set(), 0, 0
    while True:
        response = fetch(offset)
        pages += 1
        if kind == 'lever':
            items = response
        else:
            if not isinstance(response, dict) or 'jobs' not in response or response.get('error'):
                raise ValueError('Missing complete jobs array or provider error')
            items = response['jobs']
        if not isinstance(items, list):
            raise ValueError('Expected a jobs array')
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('Malformed job')
            identity = item.get('id') or item.get('jobUrl') or item.get('hostedUrl')
            if not identity or str(identity) in seen:
                raise ValueError('Missing or repeated posting identity; coverage unproven')
            seen.add(str(identity));jobs.append(item)
        if kind == 'greenhouse':
            total = response.get('meta', {}).get('total')
            if total is not None and total != len(jobs):
                raise ValueError('Catalog count disagrees with advertised total')
        if kind != 'lever' or not items:
            break
        offset += len(items)  # Follow actual returned count, including a provider-side cap.
    return {'reader': VERSION, 'provider': kind, 'pages_read': pages,
            'observed_count': len(jobs), 'end_verified': True,
            'end_basis': 'terminal empty page' if kind == 'lever' else 'official nonpaginated full jobs array',
            'jobs': jobs}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('provider', choices=['greenhouse','ashby','lever'])
    parser.add_argument('board', help='Verified official board slug; never guess it from a company name')
    parser.add_argument('--output', required=True)
    args=parser.parse_args()
    slug=urllib.parse.quote(args.board, safe='')
    roots={'greenhouse':f'https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true',
           'ashby':f'https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true',
           'lever':f'https://api.lever.co/v0/postings/{slug}?mode=json&limit=50'}
    def fetch(offset):
        url=roots[args.provider]+(f'&skip={offset}' if args.provider=='lever' else '')
        req=urllib.request.Request(url,headers={'User-Agent':'Nextmove official catalog reader'})
        with urllib.request.urlopen(req,timeout=60) as response:
            return json.load(response)
    result=enumerate_catalog(args.provider,fetch)
    result['source_url']=roots[args.provider]
    body=(json.dumps(result,ensure_ascii=False)+'\n').encode()
    Path(args.output).write_bytes(body)
    print(json.dumps({k:v for k,v in result.items() if k!='jobs'} | {'artifact_sha256':hashlib.sha256(body).hexdigest()}))


if __name__=='__main__':main()
