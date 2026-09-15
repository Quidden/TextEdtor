# Release Guide

[Documentation index](README.md) · [Changelog](../CHANGELOG.md) · [Release workflow](../.github/workflows/release.yml)

## Published release and source development

The latest published release is [v0.1.1](https://github.com/Quidden/TextEdtor/releases/tag/v0.1.1), a Windows portable startup-fix release. Its asset is `TextEdtor-v0.1.1-windows.zip`.

Telegram integration was merged after that tag. The current source still declares `0.1.1` in `src/texteditor/__init__.py`, so the window title alone does not distinguish it from the published release. Track source builds by commit until the next version is assigned.

Extract the whole archive and run `TextEdtor.exe` in the extracted application folder. This is a portable, unsigned build.

## How GitHub Actions behaves

[`.github/workflows/release.yml`](../.github/workflows/release.yml) runs on pushed `v*` tags or manual dispatch:

1. Check out the selected source ref on `windows-latest`.
2. Set up Python 3.11 and install requirements plus PyInstaller.
3. Build a windowed, folder-based application with the `src` import path and QSS/SVG assets.
4. Zip `dist/TextEdtor` as `TextEdtor-<tag>-windows.zip`, or `TextEdtor-manual-windows.zip` for a non-tag run.
5. Upload the archive as the **TextEdtor-windows** Actions artifact.
6. Publish a GitHub Release only when the run's ref type is a tag.

A normal push to `master` does not build a release. Manual dispatch on a branch creates a downloadable Actions artifact, not a GitHub Release; dispatch on a tag can publish one.

## Prepare a release

1. Select an unused version and verify the intended source commit.
2. Update `src/texteditor/__init__.py` to that version.
3. Move applicable **Unreleased** items in [CHANGELOG.md](../CHANGELOG.md) into a versioned entry and add `docs/RELEASE_NOTES_<tag>.md`.
4. Update the workflow's `body_path`: it is currently hard-coded to `docs/RELEASE_NOTES_v0.1.1.md`. Without this change, a new tag would publish the old notes.
5. Update README's download/version information and describe which Telegram features the new package actually includes.
6. Run relevant [manual checks](ARCHITECTURE.md#manual-verification), then build and launch the packaged executable. Check the known Telegram UI gaps before claiming phone login is ready.
7. Inspect the archive: include the complete generated application folder and exclude local sessions, credentials, message caches, logs, and personal images.
8. Commit the release preparation, push it, and create/push the new tag.

Example tag commands, **after replacing the version with the chosen unused tag**:

```powershell
$version = 'vX.Y.Z'
git status --short
git tag --list $version
git push origin master
git tag $version
git push origin $version
```

Do not reuse or move the existing v0.1.1 tag. After the tag run finishes, verify the release notes, asset filename, extracted contents, and startup of the downloaded package. This guide does not create or publish a new release by itself.

## Build locally

From the repository root on Windows, using the [configured virtual environment](../README.md#quick-start):

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --name TextEdtor --paths src --add-data "src/texteditor/ui/app_style.qss;texteditor/ui" --add-data "src/texteditor/ui/check_mark.svg;texteditor/ui" src/main.py
```

The folder-based output is:

```text
dist/TextEdtor/
  TextEdtor.exe
  ... supporting runtime files ...
```

Run it from a writable location. Distribute the entire folder, not just the EXE. Current-source packaging, including Telegram dependencies and login flows, needs its own smoke check; the historical v0.1.1 release only validates its earlier source.

## Runtime paths in packaged builds

`config.py` derives its root by walking three directories up from its own `__file__`. In source runs this is the repository root. In the usual PyInstaller layout with `_internal/texteditor/config.py`, it resolves to the application folder beside the EXE. Alternative bundle layouts can change the result.

Settings/session/cache/log files are created under that root's `data/`, with image files under `images/`. The app does not use an OS user-data directory. Check the actual paths during the packaged smoke check, keep the application folder writable, and inspect generated output before distributing an archive.
