# Scan official job catalogs

Input: run ID and the Target Companies snapshot. Include every company marked Allow. Exclude wins when duplicate rows conflict. Maintain a stable company ID and an approved list of official catalog sources, including separate boards or regions. Missing or unverified source configuration is a coverage gap.

For each source, use its official feed or a repeatable catalog reader. Follow every page or cursor to a verified end. Detect repeated cursors, missing pages, capped results, unexpected empty responses and mismatches with advertised counts. Record counts when the source exposes them. Use web search for source discovery and diagnosis. A search result list alone cannot establish catalog coverage.

Collect every posting before filtering on title, location or seniority. Save the employer's requisition ID (or stable source posting ID), canonical URL, title, location, full description or private description reference, and observation time. Deduplicate across boards within the company using a shared requisition ID where available. With no requisition ID, use a stable source ID or canonical URL and flag suspected cross-board duplicates. Track description retrieval failures separately so unclassified roles remain visible. Reevaluate changed postings and affected roles when the candidate criteria change.

Return inventory rows and one Scan Audit row per source, plus a company rollup:

- Complete: every configured source reached a verified end and enumeration checks passed. Zero is valid only after a verified empty catalog.
- Partial: some listings were collected or some sources verified, with unresolved gaps.
- Failed: no catalog could be verified and no usable postings were collected. Record the cause, including missing source configuration.

Keep prior observations during partial or failed runs. A posting may be marked missing from inventory only after complete coverage of its known sources. Verify live availability before an application or an Applications status change. Completeness applies to published jobs on configured official sources at scan time. Audit the source list and compare sample counts and requisitions with the live sites before relying on a new reader. Report scan failures and missing descriptions independently from fit results.

## First-pass filter and tracker output

After enumerating postings, apply the private candidate profile's broad filters for role family, seniority and geography or work arrangement. Use title and catalog metadata. Exclude only clear mismatches against explicit filters. Keep plausible adjacent titles and roles with missing metadata for the next pass. Record the first-pass decision and reason. When criteria are missing, ask for them or record which filters could be applied. Leave fit ratings blank.

Save the full scan inventory in Job Inventory when that tab is available. Upsert every verified first-pass match into the existing Applications tab using the shared job key and existing requisition ID or canonical URL. Set a new row's pipeline stage to Discovered and save company, title, location, job URL, date found and run ID. Discovered does not indicate submission or a finished CV. Preserve historical status, notes, fit decisions and prior submissions. Skip creating a second row for exact roles already tracked. Map existing headers and append missing pipeline fields during authorized setup.

Only the coordinator writes to Sheets. Publish source and company coverage, raw and unique posting counts, first-pass passes and exclusions, saved rows and unresolved sources. Verify the writes and surface any saved-row gap. If the run is interrupted, resume unfinished sources using the same run plan. If a cursor is stale, rescan that source and deduplicate.
