"""Lifecycle: Run ends at Ready; the explicit-only Submit stage moves Ready to Applied or Apply manually."""
STATUSES = ['Inventoried', 'Need review', 'Queued', 'Ready', 'Needs answer', 'Apply manually', 'Applied', 'Not pursuing', 'Duplicate']
END_STATES = {'Ready', 'Apply manually', 'Applied', 'Not pursuing', 'Duplicate'}
# Prepare takes Queued roles and re-checks Needs answer roles on every invocation.
PREPARE_INPUTS = {'Queued', 'Needs answer'}
SUBMIT_INPUTS = {'Ready'}
SUBMIT_OUTCOMES = ('Applied', 'Apply manually')
LEGACY_READ_ONLY = {'Interviewing', 'Rejected'}
# Applied is written only by Submit with verified proof; afterwards it is read-only like legacy outcomes.
PROTECTED_OUTCOMES = {'Applied'} | LEGACY_READ_ONLY
