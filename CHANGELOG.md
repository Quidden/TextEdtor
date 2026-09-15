# Changelog

[Project overview](README.md) · [Release guide](docs/RELEASE.md)

## Unreleased — current master

The source version string remains `0.1.1`, but the following changes were merged after the published v0.1.1 tag.

### Telegram integration

- Added Telethon user-session authentication services for QR, phone code, and cloud-password completion.
- Added the progressive **Telegram account** form, persistent session, and account status indicator.
- Added per-result **Push to TG**, image attachment, long-text splitting, and a local-date hashtag for Saved Messages.
- Added the **Saved Messages manager** with the latest 30 messages, media labels/text previews, text/caption editing, and direct deletion.
- Added Qt background workers, serialized client operations, local message cache, and Telegram operation logging.
- Shared replacement-rule management between the main page and Telegram manager.

### Documentation

- Refreshed the project overview and setup instructions to describe the current source and published package accurately.
- Added a Telegram UI walkthrough, real-widget screenshots with synthetic data, a documentation index, and troubleshooting.
- Updated architecture, Telegram service/storage behavior, release preparation, and issue-report guidance.

### Known limitations

- Phone-code success currently resets the code-entry UI; some phone 2FA errors do not reveal the password field. QR login is the recommended route.
- Telegram deletion is immediate; the manager has no confirmation/undo, pagination, or media playback.
- Drafts are not autosaved, the image has no clear control, and sends have no duplicate-request prevention.

See [Telegram UI](docs/TELEGRAM_UI.md) and [troubleshooting](docs/TROUBLESHOOTING.md) for details.

## v0.1.1 — 2026-05-29

Fixed packaged application startup imports, included the `src` import path and UI assets in the build, and corrected result-copy logging.

[Release notes](docs/RELEASE_NOTES_v0.1.1.md) · [GitHub release](https://github.com/Quidden/TextEdtor/releases/tag/v0.1.1)

## v0.1.0

First Windows portable release with text cleanup/replacement, splitting and copying, image conversion and file drag-out, saved settings, and application logs.

[Release notes](docs/RELEASE_NOTES_v0.1.0.md) · [GitHub release](https://github.com/Quidden/TextEdtor/releases/tag/v0.1.0)
