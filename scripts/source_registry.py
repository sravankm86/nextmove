"""Pure source freshness checks; no source edits or invented approvals."""
import hashlib
import json


def text_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def document_text(document):
    """Concatenate body text runs in provider tab/content order, preserving whitespace.

    Supports raw Docs tabs and the connector's flattened tabs. Headers, footers and
    style metadata are excluded; do not hash an independently trimmed export.
    """
    def runs(value):
        if isinstance(value, list):
            return ''.join(runs(x) for x in value)
        if not isinstance(value, dict):
            return ''
        if 'textRun' in value:
            return value['textRun'].get('content', '')
        return ''.join(runs(x) for x in value.values())
    def tabs(values):
        result = ''
        for tab in values:
            body = tab.get('body') or tab.get('documentTab', {}).get('body') or {}
            result += runs(body.get('content', []))
            result += tabs(tab.get('childTabs', []))
        return result
    return tabs(document['tabs']) if document.get('tabs') else runs(document.get('body', {}).get('content', []))


def inspect(reference, observed):
    if reference.get('file_id') != observed.get('file_id'):
        raise ValueError('Observed file differs from the registered source')
    if reference.get('use') in ('historical_only', 'archive'):
        return {'state': 'Historical only', 'usable_as_current': False}
    if not observed.get('revision') or not observed.get('text_sha256'):
        return {'state': 'Needs verification', 'usable_as_current': False}
    matches = (reference.get('revision') == observed['revision']
               and reference.get('text_sha256') == observed['text_sha256'])
    return {'state': 'Current' if matches else 'Changed', 'usable_as_current': matches}


def cache_current(cache, source):
    """A fresh registry does not magically refresh old extracted preferences."""
    return (not cache.get('cache_stale') and bool(source.get('revision'))
            and bool(source.get('text_sha256'))
            and cache.get('source_revision') == source['revision']
            and cache.get('source_text_sha256') == source['text_sha256'])
