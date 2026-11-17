"""Feedback inbox guards and frozen Review evals. No network, credentials or model calls.

The harness owns reads/writes and fresh-context Review. This helper prepares only
label-free inputs, validates predictions and scores them against a separate key.
"""
import argparse
import hashlib
import json
from pathlib import Path

VERDICTS = ('Pursue', 'Not pursuing')
# Starter categories only; a private eval registry may define its own reason types.
REASON_TYPES = ('Career fit', 'Resume fit', 'Pay', 'Location', 'Seniority', 'Company', 'Expired', 'Other')
SPLITS = ('Train', 'Holdout')
PREDICTIONS = ('Queued', 'Need review', 'Not pursuing')
_AGREE = {('Pursue', 'Queued'), ('Not pursuing', 'Not pursuing')}


def digest(value):
    raw = value if isinstance(value, str) else json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def feedback_id(stage, entity, note):
    """Same feedback on the same entity is idempotent; titles never prove identity."""
    if not stage or not entity or not note or not note.strip():
        raise ValueError('Feedback requires stage, stable entity identity and nonempty text')
    return digest([stage, entity, note.replace('\r\n', '\n').strip()])


def feedback_action(stage, entity, note, existing):
    key = feedback_id(stage, entity, note)
    same = [x for x in existing if x.get('feedback_id') == key]
    if len(same) > 1:
        raise ValueError('Duplicate feedback identities need reconciliation')
    return {'feedback_id': key, 'action': 'reuse' if same else 'capture',
            'case_id': same[0].get('case_id') if same else None}


def may_clear(stage, entity, captured_note, current_note, receipt):
    """Re-read exact text at the write boundary; a changed note is never cleared."""
    if captured_note != current_note:
        return False
    return bool(receipt.get('feedback_id') == feedback_id(stage, entity, captured_note)
                and receipt.get('case_id') and receipt.get('snapshot_ref') and receipt.get('history_id')
                and all(receipt.get(k) is True for k in ('eval_verified', 'snapshot_verified', 'history_verified')))


def outcome(verdict, prediction):
    if verdict not in VERDICTS or prediction not in PREDICTIONS:
        raise ValueError('Unknown verdict or prediction')
    if (verdict, prediction) in _AGREE:
        return 'agree'
    if prediction == 'Need review':
        return 'deferred'
    return 'false_queue' if prediction == 'Queued' else 'missed'


def score(rows, split=None):
    if split is not None and split not in SPLITS:
        raise ValueError('Unknown split')
    picked = [r for r in rows if r.get('active', True) and (split is None or r.get('split') == split)]
    counts = {'agree': 0, 'false_queue': 0, 'missed': 0, 'deferred': 0, 'unscored': 0}
    for r in picked:
        if r['verdict'] not in VERDICTS:
            raise ValueError('Unknown verdict')
        if r.get('prediction') is None:
            counts['unscored'] += 1
        else:
            counts[outcome(r['verdict'], r['prediction'])] += 1
    total = len(picked)
    positives = [r for r in picked if r['verdict'] == 'Pursue']
    queued = [r for r in picked if r.get('prediction') == 'Queued']
    return {'total': total, **counts, 'status_match': counts['agree'] / total if total else None,
            'coverage': (total - counts['unscored']) / total if total else None,
            'positive_count': len(positives),
            'positive_recall': sum(r.get('prediction') == 'Queued' for r in positives) / len(positives) if positives else None,
            'positive_deferrals': sum(r.get('prediction') == 'Need review' for r in positives),
            'queue_precision': sum(r['verdict'] == 'Pursue' for r in queued) / len(queued) if queued else None}


def prepare(dataset, split=None):
    """Only allowlisted fields enter the reviewer bundle. Labels stay in the key."""
    if split is not None and split not in SPLITS:
        raise ValueError('Unknown split')
    context = dataset['context']
    required = ('goals', 'master', 'confirmed_facts', 'instructions')
    for name in required:
        source = context[name]
        if not source.get('text') or source.get('sha256') != digest(source['text']) or not source.get('identity'):
            raise ValueError('Unfrozen or corrupt context: ' + name)
    from role_gate import review_frame_contract
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'review.md'
        path.write_text(context['instructions']['text'])
        policy, contract = review_frame_contract(path)
    blind, key, blocked, seen = [], [], [], set()
    for case in dataset['cases']:
        cid = case['case_id']
        if cid in seen:
            raise ValueError('Duplicate case ID')
        seen.add(cid)
        if not case.get('active', False) or split and case.get('split') != split:
            continue
        if case.get('verdict') not in VERDICTS or case.get('split') not in SPLITS:
            raise ValueError('Active cases require a human verdict and valid split')
        record = {'case_id': cid, 'verdict': case['verdict'], 'reason': case.get('reason', ''),
                  'reason_type': case.get('reason_type', 'Other'), 'split': case['split'], 'active': True,
                  'entity_id': case['entity_id'], 'eval_record_id': case.get('eval_record_id'),
                  'group_id': case.get('group_id', cid)}
        inputs = case.get('inputs', {})
        jd = inputs.get('jd_text')
        company = inputs.get('company', {})
        if not jd or inputs.get('jd_sha256') != digest(jd) or not company.get('evidence_identity'):
            blocked.append({'case_id': cid, 'reason': 'Missing or corrupt frozen JD/company evidence'})
        else:
            # Deliberately omit feedback, labels, split, row IDs, URLs and previous predictions.
            facts = {k: company[k] for k in ('name', 'search_status', 'funding_stage', 'facts', 'evidence_identity') if k in company}
            blind.append({'case_id': cid, 'role': inputs['role'], 'jd_text': jd, 'company': facts})
        key.append(record)
    bundle = {'schema': 'nextmove.review-replay.v1', 'policy': policy, 'review_contract': contract,
              'context': {k: {n: context[k][n] for n in ('text', 'sha256', 'identity')} for k in required},
              'cases': blind}
    bundle['comparison_sha256'] = digest({'context': {k: bundle['context'][k] for k in required if k != 'instructions'}, 'cases': blind})
    bundle['bundle_sha256'] = digest(bundle)
    answer_key = {'schema': 'nextmove.review-answer-key.v1', 'bundle_sha256': bundle['bundle_sha256'],
                  'cases': key, 'blocked': blocked, 'run_kind': 'blind_replay'}
    return bundle, answer_key


def evaluate(bundle, key, predictions):
    clean = {k: v for k, v in bundle.items() if k != 'bundle_sha256'}
    if digest(clean) != bundle.get('bundle_sha256') or key.get('bundle_sha256') != bundle['bundle_sha256']:
        raise ValueError('Bundle/key identity mismatch')
    if predictions.get('bundle_sha256') != bundle['bundle_sha256']:
        raise ValueError('Predictions belong to different frozen inputs')
    allowed = {c['case_id'] for c in bundle['cases']}
    seen, by_id = set(), {}
    from role_gate import scored_review
    for p in predictions['predictions']:
        cid = p['case_id']
        if cid not in allowed or cid in seen:
            raise ValueError('Unknown or duplicate prediction identity')
        seen.add(cid)
        if not isinstance(p.get('reason'), str) or not p['reason'].strip():
            raise ValueError('Prediction needs a reason')
        # Human targeting may end a case before fit scoring; preserve this distinction.
        company = next(c['company'] for c in bundle['cases'] if c['case_id'] == cid)
        if p.get('scope_decision') == 'Excluded':
            if company.get('search_status') != 'Exclude' or p['status'] != 'Not pursuing':
                raise ValueError('Unsupported scope decision')
        elif p.get('scope_decision') == 'Proposed':
            if company.get('search_status') != 'Proposed' or p['status'] != 'Need review':
                raise ValueError('Unsupported scope decision')
        else:
            expected = scored_review(p['career_fit'], p['resume_fit'], contract=bundle['review_contract'])['outcome']
            if p['status'] != expected:
                raise ValueError('Prediction contradicts frozen Review routing')
        by_id[cid] = p
    rows = [{**c, 'prediction': by_id.get(c['case_id'], {}).get('status'),
             'explanation': by_id.get(c['case_id'], {}).get('reason')} for c in key['cases']]
    groups = {}
    for row in rows:
        previous = groups.setdefault(row['group_id'], set())
        previous.add(row['split'])
    return {'schema': 'nextmove.review-eval-report.v1', 'bundle_sha256': bundle['bundle_sha256'],
            'answer_key_sha256': digest(key['cases']), 'kind': 'blind_replay', 'comparison_sha256': bundle['comparison_sha256'], 'policy': bundle['policy'], 'complete': len(seen) == len(key['cases']),
            'overall': score(rows), 'train': score(rows, 'Train'), 'holdout': score(rows, 'Holdout'),
            'themes': {theme: score([r for r in rows if r['reason_type'] == theme]) for theme in sorted({r['reason_type'] for r in rows})},
            'blocked': key['blocked'], 'missing_predictions': sorted(allowed - seen),
            'split_overlap_groups': [g for g, splits in groups.items() if len(splits) > 1],
            'reason_quality': 'Not automatically graded; inspect critical evidence and rubric separately.', 'rows': rows}


def compare(baseline, candidate):
    if baseline['comparison_sha256'] != candidate['comparison_sha256']:
        raise ValueError('Candidate changed cases or factual inputs, not just instructions')
    b = {r['case_id']: r for r in baseline['rows']}
    c = {r['case_id']: r for r in candidate['rows']}
    if baseline.get('answer_key_sha256') != candidate.get('answer_key_sha256') or b.keys() != c.keys() or any(b[k]['verdict'] != c[k]['verdict'] for k in b):
        raise ValueError('Answer key changed between runs')
    improved, regressed = [], []
    for cid, before in b.items():
        after = c[cid]
        old = before.get('prediction') is not None and outcome(before['verdict'], before['prediction']) == 'agree'
        new = after.get('prediction') is not None and outcome(after['verdict'], after['prediction']) == 'agree'
        if old and not new:
            regressed.append(cid)
        if new and not old:
            improved.append(cid)
    return {'improved': improved, 'regressed': regressed,
            'ready_for_human_review': bool(candidate['complete'] and improved and not regressed),
            'automatic_promotion': False}


def write_new(path, value, input_paths=()):
    """Keep frozen inputs and accepted outputs intact; exact retries are idempotent."""
    target = Path(path)
    if target.resolve() in {Path(p).resolve() for p in input_paths}:
        raise ValueError('An output cannot overwrite a frozen input')
    encoded = json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    if target.exists():
        if target.read_text() != encoded:
            raise FileExistsError('Use a new versioned output path')
        return
    target.write_text(encoded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare');p.add_argument('dataset');p.add_argument('--bundle', required=True);p.add_argument('--key', required=True);p.add_argument('--split', choices=SPLITS)
    p = sub.add_parser('score');p.add_argument('bundle');p.add_argument('key');p.add_argument('predictions');p.add_argument('--output', required=True)
    p = sub.add_parser('compare');p.add_argument('baseline');p.add_argument('candidate');p.add_argument('--output', required=True)
    args = parser.parse_args()
    read = lambda path: json.loads(Path(path).read_text())
    inputs = [args.dataset] if args.command == 'prepare' else [args.bundle, args.key, args.predictions] if args.command == 'score' else [args.baseline, args.candidate]
    write = lambda path, value: write_new(path, value, inputs)
    if args.command == 'prepare':
        bundle, key = prepare(read(args.dataset), args.split)
        if Path(args.bundle).resolve() == Path(args.key).resolve():
            raise ValueError('Reviewer bundle and answer key must be separate files')
        write(args.bundle, bundle);write(args.key, key)
    elif args.command == 'score':
        write(args.output, evaluate(read(args.bundle), read(args.key), read(args.predictions)))
    else:
        write(args.output, compare(read(args.baseline), read(args.candidate)))


if __name__ == '__main__':
    main()
