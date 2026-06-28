---
name: update-codex
description: Use when updating this codex-app Linux port from the latest upstream Codex Mac DMG, preserving local Linux patches, installing the refreshed desktop app, and publishing the tag-driven Linux release artifacts.
---

# Update Codex

Use this skill only from `/home/amwill/Applications/codex-app`.

## Contract

- Fetch the latest official upstream Mac artifact from the newest enclosure in
  `https://persistent.oaistatic.com/codex-app-prod/appcast.xml`; current feeds
  may provide a versioned `Codex-darwin-arm64-<version>.zip` rather than a DMG.
- Verify latest version/build against `https://persistent.oaistatic.com/codex-app-prod/appcast.xml`.
- Refresh `desktop/recovered/app-asar-extracted` from the downloaded artifact's
  `Contents/Resources/app.asar` using `--app-asar`, or from a DMG using
  `--dmg` when the feed/source provides one.
- Preserve Linux behavior patches in `desktop/scripts/assemble-codex-runtime.mjs`, especially:
  - Linux hidden titlebar/titlebar overlay path.
  - Linux native menu hide/remove behavior.
  - Linux external browser routing for auth and plugin/app flows.
  - Linux open-in target registry and browser-session launcher.
  - Linux pet/avatar overlay stability patches, including the X11/XWayland
    desktop launch contract required for reliable dragging and always-on-top
    behavior under GNOME Wayland sessions. The top-enforcement timer must not
    call `showInactive()` while the pet window is focused, or the pet reply
    input can lose keyboard focus. On Linux the pet window must remain
    focusable and treat an active reply editor as keyboard-interactive, so
    keystrokes go to the pet instead of the previously focused app.
  - Linux pet/avatar overlay hit testing: drag must start only from the
    `[data-avatar-mascot="true"]` target. Do not use Linux pointer passthrough
    for the pet window; on this Electron/X11 path it prevents hover/click state
    from reaching the pet, hiding reply controls and breaking drag.
  - Linux pet/avatar activity bubble sizing: preserve the enlarged tray layout,
    padding, compact message wrapping, and taller compact body height in the
    current `avatar-overlay-page-*` bundle. Do not merge or replay old one-off
    PR bundle edits over the current recovered bundle; keep this as a
    first-class assembler patch.
- Install the rebuilt runtime to `~/.local/opt/codex-desktop/<version>-<build>` and repoint `~/.local/opt/codex-desktop/current`.
- If the user asks to ship/release, commit, push `main`, tag `v<version>`, and wait for `.github/workflows/linux-release.yml` to publish assets.

## Workflow

1. Download and verify:
   - Download `appcast.xml` and use the first item as the newest arm64 release.
   - Download that item's full enclosure URL, usually a versioned
     `Codex-darwin-arm64-<version>.zip`.
   - Extract or inspect the artifact enough to confirm `Info.plist`
     `CFBundleShortVersionString`/`CFBundleVersion` and `app.asar` hash.

2. Refresh recovered bundle:
   - For current zip artifacts, extract `Codex.app/Contents/Resources/app.asar`
     and run `desktop/scripts/refresh-recovered-from-dmg.mjs --app-asar <path-to-app.asar> --output ./recovered/app-asar-extracted` from `desktop`.
   - For DMG artifacts, run `desktop/scripts/refresh-recovered-from-dmg.mjs --dmg ../Codex.dmg --output ./recovered/app-asar-extracted` from `desktop`.
   - Update `desktop/package.json`, `desktop/package-lock.json`, and tests that pin version/build metadata.
   - If minified bundle shapes drift, add new patch alternatives without removing older supported shapes.

3. Verify patch preservation:
   - `node --check desktop/scripts/assemble-codex-runtime.mjs`
   - `npm test -- --runInBand tests/linux/recovered-bundle.red.test.ts`
   - `npm run test:linux`
   - `npm run test:linux:codex-package`

4. Build and install:
   - Build with `desktop/scripts/build-codex-linux-runtime.mjs` into `desktop/out/Codex-linux-x64-codex-<version>-<build>`.
   - Copy that staged runtime to `~/.local/opt/codex-desktop/<version>-<build>`.
   - Update `~/.local/opt/codex-desktop/current`.
   - Validate desktop entries and refresh the desktop database.
   - Confirm `~/.local/share/applications/codex-desktop.desktop` and
     `~/.config/autostart/codex-desktop.desktop` launch through
     `/usr/bin/env ELECTRON_OZONE_PLATFORM_HINT=x11 ... --ozone-platform=x11`.
   - Confirm packaged Linux launchers keep that same X11 contract:
     `desktop/assets/linux/codex-deb.desktop.ejs`,
     `desktop/assets/linux/codex-appimage.desktop`, and the RPM maker's
     `desktopTemplate` setting in `desktop/forge.config.ts`.

5. Verify installed app:
   - `readlink -f ~/.local/opt/codex-desktop/current`
   - Read installed `resources/app.asar` package metadata and confirm version/build.
   - Search installed `app.asar` for preserved Linux patch markers.
   - After relaunch, inspect the live process and confirm the Codex command line
     includes `--ozone-platform=x11`; this is required before judging pet drag
     or z-order behavior.

6. Release when requested:
   - Commit with a Conventional Commit, usually `chore: refresh linux port to <version>`.
   - Push `main`.
   - Create and push annotated tag `v<version>`.
   - Watch the Linux release workflow to success.
   - Verify release assets include:
     - `codex-app-linux-x64-v<version>.AppImage`
     - `codex-app-linux-x64-v<version>.deb`
     - `codex-app-linux-x64-v<version>.rpm`
     - `codex-app-linux-arm64-v<version>.deb`

## Notes

- The repo currently has no Arch-package release lane. Do not claim one shipped unless the workflow has been extended and verified.
- Downloaded upstream artifacts, `desktop/tmp`, and `desktop/out` are generated
  inputs/outputs; do not commit them unless the repo policy changes.
- If GitHub says `release not found` immediately after tag push, watch the workflow. The release is created by the tag-driven workflow after artifacts publish.
