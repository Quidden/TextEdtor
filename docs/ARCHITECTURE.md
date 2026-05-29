# Architecture

TextEdtor is a small PyQt6 desktop application organized into UI widgets and service modules.

## Entry Point

`src/main.py` creates a `QApplication`, opens a `QMainWindow`, and mounts `MainWindowW` as the central widget.

## UI Layer

The UI lives under `src/texteditor/ui/`.

- `main_window_widget.py` composes the main layout, connects buttons to service functions, and coordinates text/image widgets.
- `text_widget.py` owns the central plain-text editor.
- `result_widget.py` displays one split text block and provides clipboard copying.
- `image_result_widget.py` handles image preview, paste/drop input, and conversion controls.
- `setting_widget.py` contains the settings tab widget.
- `setting_tabs/black_list_menu_widget.py` manages replacement rule input and deletion.
- `setting_tabs/setting_menu_widget.py` manages cleanup checkboxes and saved settings.

## Service Layer

The service modules live under `src/texteditor/services/`.

- `black_list.py` stores replacement rules in JSON, reads them back, deletes items, and applies replacements to text.
- `save_func.py` stores and loads checkbox settings.
- `text_edit.py` contains the text splitting helper.
- `app_logger.py` writes logs to `data/app.log` and mirrors them into the in-app log widget.

## Runtime Paths

`src/texteditor/config.py` defines paths relative to the repository root:

- `DATA_DIR`: `data/`
- `BLACK_LIST_FILE`: `data/black_list.json`
- `SAVE_SETTINGS_FILE`: `data/save_settings.json`
- `LOG_FILE`: `data/app.log`
- `IMAGE_DIR`: `images/`

## Data Flow

1. User edits text in `TextWidget`.
2. `MainWindowW.replace_text()` reads the text and current settings.
3. `accept_black_list()` loads replacement rules from JSON and applies replacements.
4. The cleaned text is written back into `TextWidget`.
5. `MainWindowW.text_division_result()` splits text by `=====` and creates `ResultWidget` instances.
6. User copies individual result blocks through `ResultWidget.copy_text()`.

## Known Limitations

- The split separator is currently hard-coded.
- Result rendering is limited to four text blocks.
- The project does not currently include automated tests.
- Some image conversion behavior is still marked for follow-up in the source code.
