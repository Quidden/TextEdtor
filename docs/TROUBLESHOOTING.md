# Troubleshooting

[Documentation index](README.md) · [Usage](USAGE.md) · [Telegram UI](TELEGRAM_UI.md)

## Installation and version

| Symptom | What to check |
| --- | --- |
| Telegram controls are missing | The published v0.1.1 package predates Telegram support. Use the [current source setup](../README.md#quick-start). |
| Window says 0.1.1 but Telegram is present | The source version string has not been bumped. Include `git rev-parse --short HEAD` in source-build reports. |
| `ModuleNotFoundError` when running source | Install `requirements.txt` with the same environment interpreter used to run `src/main.py`. |
| PowerShell blocks environment activation | Use `.\.venv\Scripts\python.exe` directly, as in the quick start. Activation is optional. |
| A copied virtual environment will not start | Virtual environments depend on the original Python installation. Create a fresh environment with an available Python and install requirements. |
| Packaged application fails after moving the EXE | Extract/copy the complete application folder, including its bundled supporting files. |
| A release archive triggers a Windows publisher warning | The portable build is not code-signed. Published downloads are linked from this repository's [Releases](https://github.com/Quidden/TextEdtor/releases). |

## Text and images

| Symptom | What to check |
| --- | --- |
| A rule has no effect | Matching is literal and case-sensitive. **Confirm** saves the rule; **Accept black list** applies it to the central editor. |
| Result text did not change after cleanup | Results are snapshots. Apply cleanup to the center editor, then split again. This replaces edits made in existing result blocks. |
| Empty result blocks appear | Adjacent or leading/trailing `=====` separators produce empty segments. |
| Clipboard copy fails | Inspect **Settings → Log** for the clipboard error and check that the desktop clipboard is available. |
| **Paste** says `Copy an image first` | The clipboard must contain image data, not only a file path or copied text. Alternatively, drag an image file into the panel. |
| File drag-out is unavailable | Click **Convert** first; loading an image alone does not enable dragging the converted output. |
| Previous converted image disappeared | Each format uses a fixed output filename. Copy/rename outputs you want to keep before another conversion. |
| Telegram keeps attaching the old image | The loaded image is reused on every send. There is no clear-image control yet; preserve unsaved text and restart for text-only sending. |

## Telegram login

| Symptom | What to do |
| --- | --- |
| API ID/hash error | Enter the numeric API ID and its matching API hash in **Settings → Settings**, then **Save settings**. These are Telegram application credentials. |
| Account is not signed in | Complete QR login; saving credentials alone does not authorize the account. Hover over the account dot for the check's error. |
| QR expired/timed out | Wait for the current attempt to finish and click **Generate QR code** again. |
| QR accepted but a password is requested | Enter the Telegram cloud password and click **Sign in**. Use the two-step verification password, not a local app PIN or login code. |
| Phone code does not arrive by SMS | Read the reported delivery method and check existing Telegram sessions. The UI cannot choose or force an alternate delivery method. |
| Phone code field disappears after **Send code** | Known UI issue: the success callback resets the form after the code request. Use QR login. |
| Phone 2FA error appears without a password field | Known UI issue: some two-step verification error strings do not trigger the field. Use QR login. |
| Restart does not restore phone code entry | Only the phone/code hash is persisted; the form step is not restored. Use QR login. |
| Login works until restart | Click **Save settings** to persist API credentials, and keep the runtime session file. Check that the session was not revoked in Telegram. |
| Changing the phone keeps the same account | One fixed local session is used. Changing credential fields does not switch the authorized user. |
| Telegram rate limit | Follow the wait time in the error; avoid repeated code requests or send clicks. |

The account dot reports the last check, not a continuous connection status. Checks run on startup, settings save, and successful login. A QR authorization wait can delay other Telegram operations in the same app instance.

## Sending and message management

| Symptom | What to do |
| --- | --- |
| `There is no text or image to send` | Add text to the result or load an image. |
| A send failed but content appeared | Earlier chunks or the image may have succeeded. Refresh Saved Messages before retrying to avoid duplicates. |
| A date marker appears without content | The marker is sent and saved before the content; a later send can fail. |
| The marker appears more than once | Local date-marker state may have been reset, or a separate installation may have sent another marker. |
| New messages/marker are absent from the manager | Click **Refresh**. The manager loads only the latest 30 and does not poll Telegram in the background. |
| `Showing locally saved messages` | Online synchronization failed. Displayed records are cached and may be stale; resolve the reported connection/auth error and refresh. |
| **Update in TG** is disabled | Select a text message or media with an existing caption. Uncaptioned media is read-only in this UI. |
| An edit is rejected | The app rejects empty text, text over 4,096 characters, or captions over 1,024; Telegram can also reject an unchanged or otherwise invalid edit. |
| Edit/delete reports failure but Telegram changed | The mutation may have succeeded before the subsequent history refresh failed. Click **Refresh** once connectivity returns. |
| Media has a label but no thumbnail/playback | The manager shows media type and text/caption only. Open Telegram to view the actual attachment. |
| A deleted message cannot be restored | The trash icon deletes remotely with no confirmation or undo in TextEdtor. |

Edits in the message editor are not autosaved or queued offline. A selection change, refresh, or operation result can replace them. Avoid running several TextEdtor instances against the same runtime directory; the Telegram lock only covers one process.

## Logs and useful bug reports

Open **Settings → Log** and use **Refresh log**. For source runs, the file is `data/app.log`. Report:

- OS, release tag or source commit, and whether you use an EXE or source checkout;
- affected screen/control and exact steps;
- expected result, actual result, and the displayed error;
- relevant redacted log lines and, when useful, a screenshot with private content removed.

Create a [bug report](https://github.com/Quidden/TextEdtor/issues/new?template=bug_report.md). Do not attach `data/`, API hashes, QR login codes, phone/code-hash state, session files, or private Saved Messages. See [session/storage details](TELEGRAM_INTEGRATION.md#runtime-storage).
