# Release Guide

TextEdtor releases are built by GitHub Actions.

## Current Release

The first release version is:

```text
v0.1.1
```

The downloadable Windows package is published as a GitHub Release asset:

```text
TextEdtor-v0.1.1-windows.zip
```

This package is portable. Users only need to extract the archive and run `TextEdtor.exe`.

## Create A Release

1. Make sure the working tree is clean.
2. Update `src/texteditor/__init__.py`.
3. Add or update release notes in `docs/`.
4. Commit the release changes.
5. Create and push a version tag:

```powershell
git tag v0.1.1
git push origin master
git push origin v0.1.1
```

GitHub Actions will build the Windows executable, zip it, and attach it to the GitHub Release.

## Build Locally

Local builds use PyInstaller:

```powershell
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --clean --windowed --name TextEdtor --paths src --add-data "src/texteditor/ui/app_style.qss;texteditor/ui" --add-data "src/texteditor/ui/check_mark.svg;texteditor/ui" src/main.py
```

The output appears in:

```text
dist/TextEdtor/
```
