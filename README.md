<div align="center">

# TextEdtor

**Prepare text, convert images, and send results to Telegram Saved Messages.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-41CD52?logo=qt&logoColor=white)
![Telethon](https://img.shields.io/badge/Telegram-Telethon-26A5E4?logo=telegram&logoColor=white)
[![Release](https://img.shields.io/github/v/release/Quidden/TextEdtor)](https://github.com/Quidden/TextEdtor/releases/latest)

[Getting started](#quick-start) · [Usage guide](docs/USAGE.md) · [Telegram UI](docs/TELEGRAM_UI.md) · [Documentation](docs/README.md)

</div>

TextEdtor is a PyQt6 desktop application for preparing text and images in one workspace. Clean up pasted text with saved replacement rules, split it into editable blocks, convert an image, and copy or send each result to your Telegram **Saved Messages** (Избранное).

Text and image tools work locally. The optional Telegram integration signs in to your user account through Telethon and connects when you check the account, sign in, send, refresh, edit, or delete messages.

![TextEdtor main window with editable result blocks, image tools, and settings](docs/assets/main-window.png)

*Real application widgets rendered with sample data; no Telegram account was connected for the documentation screenshots.*

## Features

| Area | What you can do |
| --- | --- |
| Text preparation | Apply saved literal replacement rules, remove leading whitespace, and collapse repeated blank lines. |
| Result blocks | Split on `=====`, edit each block, and use **Copy** or **Push to TG**. |
| Images | Paste or drop an image, convert to WebP, PNG, or JPEG, and drag the converted file into another app. |
| Telegram sign-in | Use QR login and a saved local session; phone-code services are also present, with [current UI limitations](docs/TELEGRAM_UI.md#phone-and-code). |
| Telegram sending | Send a block with the current image, split long text automatically, and add a daily `#YYYY_MM_DD` marker. |
| Saved Messages manager | Load the latest 30 messages, inspect text and media labels, edit text/captions, or delete a message. |
| Settings and logs | Save replacement rules and preferences locally; inspect activity in **Settings → Log**. |

## Download

The latest published Windows package is [TextEdtor v0.1.1](https://github.com/Quidden/TextEdtor/releases/tag/v0.1.1):

[Download TextEdtor-v0.1.1-windows.zip](https://github.com/Quidden/TextEdtor/releases/download/v0.1.1/TextEdtor-v0.1.1-windows.zip)

Extract the complete archive and run `TextEdtor.exe` inside the extracted application folder. Keep its supporting files together.

> **Version note:** v0.1.1 predates the Telegram integration. The screenshots and Telegram guides describe the current `master` source. Run from source to use those features. The source version string still reads `0.1.1`; see the [changelog](CHANGELOG.md) for the distinction.

## Quick Start

Python **3.11+** is the documented baseline; the Windows release workflow uses Python 3.11. Run these commands from a terminal with Git and Python available.

### Windows / PowerShell

```powershell
git clone https://github.com/Quidden/TextEdtor.git
cd TextEdtor
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py
```

These commands use the environment's interpreter directly, so PowerShell script activation is optional.

### Linux / macOS source setup

```bash
git clone https://github.com/Quidden/TextEdtor.git
cd TextEdtor
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py
```

A graphical desktop and working Qt installation are required. Published binaries are Windows-only; Linux/macOS packaging is not provided.

## How It Works

1. Paste text into **General Text Editor**.
2. Add search/replacement pairs in **Settings → Black list** and click **Confirm**.
3. Choose cleanup options in **Settings → Settings**, then click **Accept black list**.
4. Separate sections with `=====` and click **Split text**.
5. Edit individual result blocks and click **Copy**, or sign in to Telegram and click **Push to TG**.
6. For images, use **Paste** or drag a file into **Image result**, choose a format, and click **Convert**.
7. Open **Telegram manager** to refresh, edit, or delete Saved Messages.

See the [usage guide](docs/USAGE.md) for examples and the behavior of each control.

## Telegram UI

Enter your API ID/hash in **Settings → Settings → Telegram account**, click **Save settings**, and use **Generate QR code**. After scanning, complete the cloud-password step if requested. The indicator below **General Buttons** shows the account connection state.

Each result's **Push to TG** sends its current text and the currently loaded image. **Telegram manager** opens a separate page with a message list, a text/caption editor, and the shared replacement-rule panel.

![Saved Messages manager with sample text, photo caption, and document rows](docs/assets/telegram-manager.png)

*Sample messages are shown for documentation. Media rows display type labels and text; the manager does not render image/video previews.*

- [Telegram UI guide](docs/TELEGRAM_UI.md): setup, QR/phone flows, status colors, sending, editing, and deletion.
- [Telegram integration reference](docs/TELEGRAM_INTEGRATION.md): services, workers, session storage, message records, and limits.
- [Troubleshooting](docs/TROUBLESHOOTING.md): sign-in issues, cached history, and sending errors.

## Runtime Files

For source runs, local files live under the repository root:

| Path | Purpose |
| --- | --- |
| `data/black_list.json` | Saved replacement rules. |
| `data/save_settings.json` | Cleanup preferences and Telegram API ID/hash/phone. |
| `data/telegram_user.session` | Authorized Telegram session. |
| `data/telegram_login.json` | Temporary phone-login state. |
| `data/telegram_state.json` | Last daily hashtag sent. |
| `data/telegram_messages.json` | Cached Saved Messages text and metadata. |
| `data/app.log` | Application logs. |
| `images/` | Pasted images and converted files. |

`data/`, `images/`, and session files are ignored by Git. Settings and the message cache are stored as plaintext; TextEdtor does not encrypt the session. Keep these files private and exclude them from screenshots, bug reports, and release archives. See [storage and session details](docs/TELEGRAM_INTEGRATION.md#runtime-storage).

## Documentation

| Guide | Contents |
| --- | --- |
| [Documentation index](docs/README.md) | Choose a guide by task. |
| [Usage](docs/USAGE.md) | Text, images, settings, and logs. |
| [Telegram UI](docs/TELEGRAM_UI.md) | Screens, buttons, and user workflows. |
| [Telegram integration](docs/TELEGRAM_INTEGRATION.md) | Technical behavior and storage. |
| [Architecture](docs/ARCHITECTURE.md) | Source layout and data flow. |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Known limitations and recovery steps. |
| [Release guide](docs/RELEASE.md) | Local builds and GitHub Actions publishing. |
| [Changelog](CHANGELOG.md) | Released and unreleased changes. |

## Development

The code is in `src/texteditor/`, with Qt widgets in `ui/` and application logic in `services/`. Dependencies are pinned in [requirements.txt](requirements.txt).

There is no automated test suite yet. Before shipping a change, follow the [manual verification checklist](docs/ARCHITECTURE.md#manual-verification). Report reproducible problems through [GitHub Issues](https://github.com/Quidden/TextEdtor/issues), including the release or source commit and the affected screen.
