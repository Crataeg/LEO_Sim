# Sensitive Scan Report

Generated at: 2026-05-07T22:25:45.5811211+08:00

Read-only scan only. No files were cleaned, deleted, renamed, rewritten, masked, or otherwise modified by the scan. The report records paths and keywords/pattern names only; matched secret values or source lines are intentionally not copied into this report.

## Scope

- Excluded: .git internal directory and this generated SENSITIVE_SCAN_REPORT.md file.
- Content scan: git grep over text files, including untracked and normally ignored files, with core.longpaths=true and core.quotePath=false.
- Path scan: UPLOAD_MANIFEST.csv relative paths.
- Binary/compressed file contents are not expanded by git grep; their paths are still checked for the requested keywords.

## Requested Keywords

- token
- password
- passwd
- secret
- api_key
- apikey
- github_pat
- private_key
- ssh-rsa
- BEGIN OPENSSH PRIVATE KEY
- BEGIN RSA PRIVATE KEY
- access_key
- refresh_token
- client_secret

## Summary

- Content keyword hit rows: 813
- Unique content keyword files: 645
- Path keyword hit rows: 27
- Unique path keyword files: 27
- High-risk credential pattern rows: 0
- Unique high-risk credential files: 0
- Push block required by high-risk scan: NO
- Full keyword hit CSV: docs_auto_generated/sensitive_keyword_hits.csv
- Git grep error log bytes: 0

## High-Risk Credential Files

- None detected by high-risk literal/pattern scan.

## Notes

- Generic words such as token/password/secret can appear in library code, examples, papers, logs, or generated documentation without being actual credentials. Those are preserved in the full CSV as keyword hits for review.
- High-risk rows are the rows that resemble actual credentials or private-key markers and are used for the push blocking decision.
- The GitHub token prefix detector requires a non-token boundary before ghp_/gho_/ghu_/ghs_/ghr_ so ordinary words such as highs_ in SciPy are not treated as GitHub tokens.
