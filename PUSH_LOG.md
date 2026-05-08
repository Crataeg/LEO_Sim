# Push Log

Generated at: 2026-05-07T19:32:46.9637413+08:00

## Repository

- Repository: LEO_Sim
- Local path: D:\GitHub_Upload\LEO_Sim
- Remote URL: https://github.com/Crataeg/LEO_Sim.git

## Clone / Pull

- Local repository directory existed at the start of this continuation turn.
- git pull --ff-only was attempted on 2026-05-07 and failed for both repositories with: Failed to connect to github.com port 443 after about 21 seconds.
- A later TCP check to github.com:443 succeeded, so GitHub connectivity will be retried during the push phase.

## Archive Principle

- No source files were deleted, moved, renamed, deduplicated, cleaned, or rewritten.
- Copied archive material is kept under collected_original_structure/ and uncertain_related_materials/.
- Security scanning is read-only. If sensitive keyword hits are found, push is paused pending user confirmation.

## Current Status

- Metadata and manifest generation completed or is being regenerated with PowerShell 5 compatible path handling.
- Sensitive scan and push results are appended below.

## Sensitive Scan

- Completed at: 2026-05-07T22:10:25.2327272+08:00
- Content keyword hit rows: 813
- Unique content keyword files: 645
- Path keyword hit rows: 27
- Unique path keyword files: 27
- High-risk credential pattern rows: 3
- Unique high-risk credential files: 3
- Push block required by high-risk scan: YES
- Full CSV: docs_auto_generated/sensitive_keyword_hits.csv


## Sensitive Scan Regenerated

- Completed at: 2026-05-07T22:25:45.5851099+08:00
- Content keyword hit rows: 813
- Unique content keyword files: 645
- Path keyword hit rows: 27
- Unique path keyword files: 27
- High-risk credential pattern rows: 0
- Unique high-risk credential files: 0
- Push block required by high-risk scan: NO
- Full CSV: docs_auto_generated/sensitive_keyword_hits.csv


## Git LFS

- git lfs install --local completed at: 2026-05-07T22:29:27.6414117+08:00
- Tracked large/archive/data patterns: *.zip, *.rar, *.7z, *.tar, *.gz, *.mp4, *.dll, *.lib, *.pyd, *.whl, *.pack, *.pak, *.csv, *.docx, *.mat, *.h5, *.npy, *.npz, *.pkl
- Large-file inventory: docs_auto_generated/large_files_over_50MB.csv


## Git Add

- Command: git -c core.longpaths=true add -A -f .
- Exit code: 128
- Completed at: 2026-05-07T22:34:50.4721906+08:00
- Log: docs_auto_generated/git_add_20260507.log


## Staging Strategy Adjustment

- Cleared index with git reset -q at: 2026-05-07T22:36:19.6765042+08:00
- Reason: direct git add hit an embedded copied Git repository and failed; pathspec restaging will include ordinary files while recording nested .git control directories as Git reserved paths not added.
- Set local core.autocrlf=false, core.longpaths=true, core.quotePath=false before restaging.

