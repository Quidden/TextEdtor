---
name: Bug report
about: Report a reproducible problem in the editor, image tools, or Telegram UI
title: "[Bug] "
labels: bug
assignees: ""
---

## Description

Describe the problem and the affected screen/control. Check [troubleshooting](https://github.com/Quidden/TextEdtor/blob/master/docs/TROUBLESHOOTING.md) for current limitations.

## Steps to Reproduce

1. Open…
2. Enter/click…
3. Observe…

## Expected Result

What should have happened?

## Actual Result

What happened instead? Include the exact status/error text.

## Environment

- OS:
- Windows EXE or source checkout:
- Release tag or source commit (`git rev-parse --short HEAD`):
- Python version (source runs):
- PyQt6 / Telethon versions (if relevant):

The source still uses version string 0.1.1 after adding Telegram support; include the commit when reporting a source build.

## Telegram Context (if relevant)

- QR or phone-code login:
- Two-step verification enabled (yes/no):
- Operation: sign-in / send / refresh / edit / delete:
- Text only, image caption, or other media:
- Did Telegram apply the operation despite an error in the app?

## Logs or Screenshots

Paste only relevant, redacted lines from **Settings → Log**. Remove private text, local paths, and account identifiers from screenshots/logs.

Do not attach `data/`, session files, API hashes, login codes, QR login images, passwords, or private message caches.
