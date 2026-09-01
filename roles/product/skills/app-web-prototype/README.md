# app-web-prototype

> **Original author: 花叔 · 花生 (alchaincyf)** — derived from
> [huashu-design](https://github.com/alchaincyf/huashu-design) at commit `a790f70`, MIT licensed,
> Copyright (c) 2026 alchaincyf. Split out and adapted for Claude Cowork by SuperTurbo.
> See NOTICE.md for the full provenance and LICENSE for the terms.

A prototype somebody can click. If the buttons do not do anything, it has not finished.

## What it does

Builds a high fidelity clickable app or web prototype as a single self contained HTML file, with
working navigation, real state and a proper device frame. Opens on a double click of a `file://`
path. Not production code, and not static pictures of screens.

Ships frames for iOS, Android, a browser window and a macOS window, so the prototype is presented
in the context it would really live in rather than floating on a white page.

## The architecture decision it makes for you

Single file by default: React with Babel inlined, local images base64 embedded. It only splits
into multiple files past roughly 1000 lines, and when it does it includes the
`python3 -m http.server` instruction, because Babel fetches over XHR and CORS blocks that on
`file://`. That failure is silent and confusing, which is why the rule is baked in rather than
left to be rediscovered.

`references/react-setup.md` holds the three rules that break the build if ignored.

## Runtime

Zero install. React and Babel load from CDN into the page; rendering and verification use the
container's Chromium. No npm install, no API keys, no sibling skill required.

## Files

    SKILL.md                            the skill itself
    assets/ios_frame.jsx                iOS device frame
    assets/android_frame.jsx            Android device frame
    assets/browser_window.jsx           browser chrome
    assets/macos_window.jsx             macOS window chrome
    assets/animations.jsx               transition and micro interaction helpers
    assets/design_canvas.jsx            pan and zoom canvas for multi screen layout
    references/app-prototype.md         flow, state and navigation patterns
    references/react-setup.md           the three build breaking rules
    references/verification.md          the render and measure gate
    references/typography.md            type scales and pairing
    references/design-styles.md         the style catalogue
    references/brand-asset-protocol.md  handling real logos and brand colours
    references/tweaks-system.md         live control panels
    references/content-guidelines.md    what earns a place

## Adjusting it

    cd app-web-prototype && zip -r app-web-prototype.skill . -x '.*' -x 'app-web-prototype.skill'

Keep LICENSE and NOTICE.md in the archive. MIT requires the copyright notice to travel with
modified versions.
