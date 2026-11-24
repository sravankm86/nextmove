"""Active lifecycle ends at a Prepare handoff; later legacy outcomes are read-only."""
STATUSES = ['Inventoried', 'Need review', 'Queued', 'Ready', 'Needs answer', 'Apply manually', 'Not pursuing', 'Duplicate']
END_STATES = {'Ready', 'Apply manually', 'Not pursuing', 'Duplicate'}
# Prepare takes Queued roles and re-checks Needs answer roles on every invocation.
PREPARE_INPUTS = {'Queued', 'Needs answer'}
LEGACY_READ_ONLY = {'Applied', 'Interviewing', 'Rejected'}
