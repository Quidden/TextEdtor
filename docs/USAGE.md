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

Click **Button2** to split the current editor content. The application displays up to four result blocks. Each block has a **Copy** button.

## Image Conversion

The image widget supports clipboard paste and drag-and-drop for common image formats.

1. Copy an image to the clipboard or drag an image file into the image area.
2. Select the output format: WebP, PNG, or JPEG.
3. Click **Result**.

The converted image is written to `images/` using a format-specific filename such as `image.webp`, `image.png`, or `image.jpeg`.

## Logs

Open **Settings -> Log** to see application events. The same events are also appended to:

```text
data/app.log
```
