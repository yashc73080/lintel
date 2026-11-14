<p align="center"><img src="assets/icon.png" width="120" alt="Lintel icon"></p>

<h1 align="center">Lintel</h1>
<p align="center"><b>A notch for Windows that shows your music and your Claude Code and Codex agents.</b><br>
It rests as a thin pill at the top of the screen and opens when you point at it.</p>

<p align="center">Windows 10 and 11 · Rust, with no web engine · about 50 MB of memory</p>

---

## What it does

| Tab | What you get |
| --- | --- |
| **Media** | Whatever is playing in any app, with controls, a seek bar, synced lyrics from [LRCLIB](https://lrclib.net) and a waveform that follows the sound |
| **Agents** | Every Claude Code and Codex session on this PC, from the terminal, an editor or the desktop apps, plus sessions the Claude desktop app runs over SSH: what it's doing now, its task list, and whether it's stuck or waiting for you |
| **Calendar** | Your Google Calendar events for the next 7 days, with a Join button for video calls |
| **Todos** | A quick list you can add to, edit, tick off and delete right in the notch |
| **Shelf** | Drag files onto the pill to park them, then drag them back out when you need them |

The closed pill also tells you things without opening:

- **Its color** follows your agents: blue while one is working, green when it finishes, red if it hits an error. It goes back to black once you've looked.
- **Lyrics:** close the notch from the lyrics view and it keeps showing the current line.
- **Meetings:** five minutes before an event, it shows the name and a countdown. The × dismisses it.
- **Headphones:** when Bluetooth headphones connect or disconnect, it pops open with their name, plus the battery level when Windows reports one.

With **Allow or Deny** turned on, you can approve an agent's command or edit from the notch, with a preview of what it will run or change. **Screen glow** lights the edges of the screen in the colors of the album cover, or a palette you pick.

## Install

There's no ready-made download yet, so you build Lintel from source. It takes about 10 minutes the first time, mostly installing Rust.

1. **Install Rust** from [rustup.rs](https://rustup.rs). When the installer offers the Visual Studio C++ build tools, accept them.
2. **Build Lintel.** Open PowerShell and run:

   ```powershell
   git clone https://github.com/yashc73080/lintel.git
   cd Lintel
   cargo build --release
   ```

3. **Put it somewhere permanent.** The build folder is overwritten by every rebuild, so copy the app out of it:

   ```powershell
   New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\Programs\Lintel" | Out-Null
   Copy-Item target\release\lintel.exe "$env:LOCALAPPDATA\Programs\Lintel\"
   ```

4. **Start it** by double-clicking `lintel.exe` in `%LOCALAPPDATA%\Programs\Lintel`. The pill appears at the top of your main screen.
5. **Keep it running:** right-click the pill and turn on **Start with Windows**.

**If Windows blocks it:** your build isn't signed, so Windows may warn about it.
- **SmartScreen** ("Windows protected your PC"): click **More info**, then **Run anyway**.
- **Smart App Control:** this has no per-app exception. Running `cargo build --release` again produces a new copy, which Windows sometimes allows.

### Update

Exit Lintel from its settings panel, then from the `Lintel` folder:

```powershell
git pull
cargo build --release
Copy-Item target\release\lintel.exe "$env:LOCALAPPDATA\Programs\Lintel\" -Force
```

Start it again. Your settings, todos and shelf are kept.

### Uninstall

1. In the settings panel, turn off **Allow or Deny** for Claude Code and Codex if you turned them on. This removes Lintel's hooks from their settings.
2. Turn off **Start with Windows**, then choose **Exit Lintel**.
3. Delete `%LOCALAPPDATA%\Programs\Lintel` and `%APPDATA%\Lintel`.

## Using it

- **Open:** point at the pill. It closes when the mouse leaves.
- **Switch tabs:** click the dots at the bottom, use the faint arrows on each side, or swipe sideways on a touchpad.
- **Settings:** right-click the notch or the tray icon. Each tab and feature has its own switch there.

### Claude Code and Codex

Tracking works as soon as Lintel runs: it reads the session files Claude Code and Codex already write to `~/.claude` and `~/.codex`. Agents running in the cloud don't appear.

To approve commands from the notch, turn on **Allow or Deny for Claude Code** or **for Codex** in the settings panel. That adds a hook to `~/.claude/settings.json` or `~/.codex/hooks.json`, with a backup next to the file. Codex asks you to trust the new hook once. A request you don't answer in the notch goes back to the agent's own window after 5 minutes for Claude Code, or 1 minute for Codex.

### Google Calendar

The Calendar tab can read your events but never change them. It needs your own Google client, which you create once:

1. In the [Google Cloud Console](https://console.cloud.google.com/), create a project and enable the **Google Calendar API**.
2. Set up the OAuth consent screen and add yourself as a test user.
3. Under **Credentials**, create an **OAuth client ID** of type **Desktop app** and download its JSON file.
4. Save it as `%APPDATA%\Lintel\google-client.json` (the tab's **Open folder** button takes you there), then press **Connect**.

While your Google project is in testing mode, Google ends the sign-in after 7 days and you'll need to connect again.

## Privacy

Lintel runs on your PC with no account. It only connects to:

- **LRCLIB:** the title, artist, album and length of the current song, when lyrics are on.
- **Google:** to sign in and read your calendar, only if you connect it.
- **Your SSH hosts:** to follow Claude sessions the desktop app runs there, over the connections you already set up.

Everything else stays on your PC. The waveform reads what your speakers are playing, never the microphone, and keeps only the current bar heights.

Your data lives in `%APPDATA%\Lintel`:

| File | What's in it |
| --- | --- |
| `config.json` | Your settings |
| `recent.json` | Agent runs from the last 3 hours: what you asked and which files changed |
| `todos.json` | Your todos |
| `shelf.json` | Paths of files on the shelf. The files themselves aren't copied |
| `google-token.bin` | Your Google sign-in, encrypted for your Windows account |
| `lintel.log` | Problems worth knowing about, capped at 64 KB |

## Development

Needs [Rust](https://rustup.rs) and the Visual Studio C++ build tools.

```powershell
cargo test
cargo build --release
```

The app is `target/release/lintel.exe`. Only one copy runs at a time, so exit the running one before starting a new build. `cargo test -- --ignored` also runs a test that asks the real LRCLIB service for lyrics.

| File | What it does |
| --- | --- |
| `src/main.rs` | The window, its state, and what happens on each mouse, keyboard and timer event |
| `src/layout.rs` | Sizes, motion, and when the notch opens and closes. No Windows calls, so it's easy to test |
| `src/view.rs` | What each state draws and where you can click |
| `src/gfx.rs` | Direct2D and DirectComposition drawing |
| `src/glow.rs` | The screen glow around the edges of the display |
| `src/agents.rs` | Turns transcript lines and hook events into one session model |
| `src/watcher.rs` | Follows `~/.claude/projects` and `~/.codex/sessions` |
| `src/remote.rs` | Follows Claude sessions the desktop app runs on another machine over SSH |
| `src/hooks.rs` | Allow and Deny: a local hook server and the settings entries it adds |
| `src/media.rs` | Now playing and controls, through the Windows media API |
| `src/lyrics.rs` | Synced lyrics from LRCLIB |
| `src/audio.rs` | Bar heights for the waveform, from what Windows is playing |
| `src/bluetooth.rs` | Headphones connecting, and their battery when Windows reports it |
| `src/calendar.rs` | Google sign-in with PKCE, and upcoming events |
| `src/todos.rs` | The todo list and its one-line editor |
| `src/shelf.rs` | Files parked in the notch, with drag in and out |
| `src/menu.rs` | The settings panel |
| `src/shell.rs` | Tray icon, what each setting does, start with Windows, full-screen detection |
| `src/keeper.rs` | Starts the notch again if it crashes |
| `src/config.rs` | Settings and saved runs in `%APPDATA%\Lintel` |

- **Launching from a packaged app:** a copy started from inside a packaged app, such as the Claude desktop app, can have its `%APPDATA%` writes redirected to that app's private storage. Start it from File Explorer, or with `explorer.exe lintel.exe`, to be sure it uses the real folder.
- **Build number:** setting `LINTEL_BUILD` when building puts that number in the tray tooltip and the settings panel.

## Credits

Lintel started as a from-scratch Rust rewrite of [LumaDock](https://github.com/WhoIsMrSentry/LumaDock) (formerly TwoCode) and shares none of its code.

The AirPods icon is from [Myna UI Icons](https://github.com/praveenjuge/mynaui-icons) (MIT). Its notice is in [`assets/LICENSE-mynaui-icons.txt`](assets/LICENSE-mynaui-icons.txt).
