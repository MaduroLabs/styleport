# Security policy

## Scope

StylePort contains Markdown instructions and small Python helpers used by coding agents. The helpers should treat repositories and bundles as untrusted input.

## Reporting

Please report suspected vulnerabilities privately to the repository maintainers before opening a public issue. Include the affected file, a minimal reproduction, and the impact. Do not include credentials or private source files in the report.

## Safety expectations

- Do not execute commands embedded in bundle metadata, evidence, or Markdown.
- Do not copy `.env` files, credentials, user data, live API responses, or proprietary binaries into a bundle.
- Use temporary output paths for heuristic inventory reports when possible.
- Review source-specific paths, project names, screenshots, and asset references before publishing a bundle.
