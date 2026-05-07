<div align="center">

# TextEdtor

Desktop helper for cleaning, splitting, replacing text fragments, and converting images.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-6.10-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Desktop-555555?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20development-F2A900?style=for-the-badge)

</div>

## Overview

**TextEdtor** is a small PyQt6 desktop application for everyday text preparation. It combines a plain-text editor, configurable replacement rules, quick text splitting, image conversion, settings persistence, and an in-app log panel.

The project is lightweight and local-first: settings, replacement rules, logs, and converted images are stored in repository-local runtime folders.

## Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Runtime Files](#runtime-files)
- [Documentation](#documentation)
- [Development](#development)

## Features

| Area | What it does |
| --- | --- |
| Text editor | Provides a central plain-text editing area for pasted or typed content. |
| Replacement rules | Stores blacklist/whitelist pairs and applies them to the current text. |
| Text cleanup | Can remove leading spaces and collapse repeated empty lines. |
| Text splitting | Splits text by the `=====` separator and shows result blocks with copy buttons. |
| Image conversion | Converts pasted or dropped images to WebP, PNG, or JPEG. |
| Logging | Writes events to both the in-app log tab and `data/app.log`. |
| Persistence | Saves replacement rules and checkbox settings as JSON files. |

## Quick Start

Clone the repository:

```powershell
git clone <repository-url>
cd TextEdtor
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python src/main.py
```

On Linux or macOS, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## How It Works

1. Paste or type text into **General Text Editor**.
2. Add replacement rules in **Settings -> Black list**.
3. Enable cleanup options in **Settings -> Settings** if needed.
4. Click **Accept black list** to apply replacements and cleanup.
5. Split text with **Button2** using the `=====` separator.
6. Copy result blocks with the **Copy** button.
7. Paste or drop an image, choose WebP, PNG, or JPEG, and click **Result**.

## Project Structure

```text
src/
  main.py
  texteditor/
    config.py
    services/
      app_logger.py
      black_list.py
      save_func.py
      text_edit.py
    ui/
      main_window_widget.py
      text_widget.py
      result_widget.py
      image_result_widget.py
      setting_widget.py
      setting_tabs/
```

## Runtime Files

The application creates local runtime files while it is used:

| Path | Purpose |
| --- | --- |
| `data/black_list.json` | Replacement rules. |
| `data/save_settings.json` | Saved checkbox settings. |
| `data/app.log` | Application logs. |
| `images/` | Converted image output files. |

These folders are ignored by Git because they contain local user data and generated output.

## Documentation

- [Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)

## Development

The project currently does not include an automated test suite. For now, the main verification flow is manual:

```powershell
python src/main.py
```

Recommended checks before publishing changes:

- the application starts without import errors;
- replacement rules can be added and applied;
- text can be split by `=====`;
- result blocks can be copied;
- settings are saved and loaded;
- image conversion writes output into `images/`.

