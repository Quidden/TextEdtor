# TextEdtor v0.1.1

Patch release for the Windows portable build.

## Fixed

- Fixed the packaged executable failing at startup with `ModuleNotFoundError: No module named 'src.texteditor...'`.
- Updated the PyInstaller build command to include `src` as an import path.
- Packaged QSS and SVG UI assets under the package-relative path used by the application.
- Fixed result block copy logging to use the current logger API.

## Download

Download `TextEdtor-v0.1.1-windows.zip` from this release, extract it, and run `TextEdtor.exe`.
