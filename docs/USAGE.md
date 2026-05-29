# Usage Guide

## Text Cleanup

The main text workflow is built around the central **General Text Editor** panel.

1. Paste or type the text into the editor.
2. Open **Settings -> Black list**.
3. Add a replacement rule:
   - `Blacklist Item`: text fragment to search for;
   - `Whitelist Item`: replacement value.
4. Click **Confirm** to save the rule.
5. Enable cleanup options in **Settings -> Settings** when needed:
   - **Text settings** removes leading spaces from each line.
   - **Empty text settings** collapses repeated empty lines.
6. Click **Save settings** to persist the checkbox state.
7. Click **Accept black list** to apply replacements and cleanup to the current text.

## Text Splitting

Text is split by the exact separator:

```text
=====
```

Example:

```text
First block
=====
Second block
```

Click **Split text** to split the current editor content. Each result block has a **Copy** button.

## Image Conversion

The image widget supports clipboard paste and drag-and-drop for common image formats.

1. Copy an image to the clipboard or drag an image file into the image area.
2. Select the output format: WebP, PNG, or JPEG.
3. Click **Convert**.

The converted image is written to `images/` using a format-specific filename such as `image.webp`, `image.png`, or `image.jpeg`.

After conversion, drag the preview area out of the app to copy the converted image file into Explorer or another application that accepts dropped files.

## Logs

Open **Settings -> Log** to see application events. The same events are also appended to:

```text
data/app.log
```

The log tab updates automatically when the log file changes. Use **Refresh log** if you want to reload it manually.
