# FS S3FS Next

Independent maintenance fork of PyFilesystem/s3fs. Preserve upstream LICENSE,
author credits, and history. Keep `fs_s3fs` imports and the `fs.opener` s3 entry
point compatible. Distribution name: `fs-s3fs-next`; Python >=3.10.

- Use English commit messages.
- Depend on fs-next, never on the original fs distribution.
- Explain fs/fs-next and fs-s3fs/fs-s3fs-next installation conflicts.
- Run isolated installed-wheel contract tests before releasing.
- Report Moto coverage separately from live AWS validation.
- Publish only when requested and ownership is configured. Never store tokens.
