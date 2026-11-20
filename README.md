# Weather Hub

<img src="icon-512.png" width="96" align="right" alt="Weather Hub icon">

Kitchen weather station for an iPad mini 1 (iPad2,5, iOS 9.3.5) that is otherwise
useless. The iPad is a thin client: one static page on GitHub Pages, every number
fetched by the device itself.

**Live: <https://rulac.github.io/weather-hub/>**

## Installing it on the iPad

1. Open <https://rulac.github.io/weather-hub/> in **Safari**.
2. Tap **setup** in the footer and press **Instaliraj profil**. Without the
   profile the page cannot reach any weather API — iOS 9 has none of the roots
   these services use. Confirm the install in Settings.
3. **Share → Add to Home Screen.** Open the app from the icon, not from Safari;
   only then does it run fullscreen without an address bar.
4. Optional: **Settings → Accessibility → Guided Access** and triple-click the
   Home button inside the app, so nobody wanders off.
5. **Settings → Display & Brightness → Auto-Lock → Never.**

iOS caches home-screen icons: after an icon change, remove the icon and add it
again.

## On screen

| Block | Content |
|---|---|
| Places | favourite places, `+` opens the picker |
| Now | glyph, temperature, condition, wind, humidity, sunrise/sunset and civil twilight |
| Hours | the next 24 hours: icon, temperature, wind, chance of rain |
| Days | icon, daily high and low, wind, `±n` from 2 °C when the models disagree |
| Clock | current time under the weather icon |
| `SATI I DANI` / `PO SATIMA` / `PO DANIMA` | switch between the forecast and the two comparison screens |
| Comparison | one row per provider: by the hour, icon + temperature; by the day, icon + high/low; both end with a `±` spread from 2 °C |
| Normals | monthly averages above the daily comparison, with the 8-day departure |
| Footer | refresh, data age and a one-word status, legend, setup, version, language |

Weekends are tinted, today is marked, the screen dims between 22:00 and 07:00
(a tap lifts it for a minute), and everything is translated to Croatian and
English. Icons follow the sun: clear and partly cloudy are a moon after dark.
Tapping the data age opens a **log** with timestamped lines about every source.
The hourly strip scrolls sideways on a narrow screen; each comparison screen
scrolls down on its own.

## Where the data comes from

All of it is fetched by the iPad, one place at a time. The seven starting places
live in `index.html`; every number is cached per place in `localStorage`.

| Source | Horizon | How |
|---|---|---|
| ECMWF IFS 0.25 | 15 days | Open-Meteo — drives the hours and the days |
| ICON (DWD) | 7 days | Open-Meteo |
| KNMI HARMONIE | 5 days | Open-Meteo |
| DMI HARMONIE | 5 days | Open-Meteo |
| MET Norway (Yr.no) | 10 days | `api.met.no`, aggregated to local days on the device |
| Meteoblue | 14 days | key typed in the setup panel |

The home screen is not an average: the **setup** panel picks the model that
drives the current block, the hours and the days — ECMWF by default, DWD, KNMI
or DMI on request. Only the Open-Meteo models have an hourly line, so Yr.no and
Meteoblue stay in the daily comparison.

Each source is refreshed on its own: a dead or slow one never holds back the
numbers that did arrive, and its row stays in the table, dimmed.

### Quota and keys

Open-Meteo counts models and variables against a daily allowance. A place is
refetched at most every ten minutes, the background tick is fifteen by default
and adjustable in **setup** from *now* in five-minute steps, and a 429 suspends
requests for half an hour — the footer then reads `podaci: … · kvota`.

Meteoblue is optional and needs a free key, typed on the device and stored in
`localStorage`; no server ever holds it:

| Service | Where |
|---|---|
| Meteoblue | register at <https://www.meteoblue.com>, then *My Account → API* |

The legend shows whether the Meteoblue key is set: without it the provider is
not used, with it its row appears in the daily comparison.

Saving a key calls the service once and prints `key works` or `key rejected
(HTTP …)` under the field.

## Places and favourites

Favourites are exactly the chips on the strip — nothing else. Removing the last
one leaves just the `+`.

Three characters in the picker query `geocoding-api.open-meteo.com`; picking a
result **shows it without adding it to the strip**, the star decides that, and
places added this way can be removed with the `×`.

## Updating the app

There is no service worker and Pages serves HTML with `max-age=600`, so the page
polls `index.html?t=…` every ten minutes and on resume, compares
`<meta name="app-version">` with the running one and navigates to
`index.html?v=<version>`. A failed attempt expires after ten minutes.

**Bump `app-version` in every commit that changes `index.html`.** Tapping `v…` in
the footer forces a cache-busted reload — the way out when the iPad is stuck.

## The profile

`trust.mobileconfig` adds ISRG Root X1/X2 and the Google Trust Services roots.

Try the button in the **setup** panel first; some iOS builds install a
mislabeled profile. If Safari only displays the file, GitHub Pages is sending
`application/octet-stream` and only a server you control can set the right type:

```bash
python3 scripts/serve_profile.py     # prints http://<lan-ip>:8123
```

Profiles survive reboots; they disappear on a wipe or manual removal.

## iOS 9.3.5 / Safari 9.1

| Feature | Support |
|---|---|
| Service Worker, PWA manifest, `fetch`, ES modules | no |
| CSS Grid, `position: sticky`, `object-fit` | no |
| Add to Home Screen, fullscreen, `localStorage` | yes |

Flexbox trims trailing whitespace at the end of an anonymous item, so label and
value pairs are always wrapped in a single element. `localStorage` is blocked
when Safari blocks cookies, so every read goes through a wrapper with a memory
fallback.

## Files

| Path | Purpose |
|---|---|
| `index.html` | the whole app: markup, styles, ES5 logic, i18n |
| `icons.js` | SVG icon set, shared with the legend |
| `normals.json` | monthly climate normals, rebuilt by hand |
| `trust.mobileconfig` | roots missing from iOS 9 |
| `icon*.png`, `favicon.png` | icons, drawn by `scripts/make_icons.py` |
| `v.html` | redirect kept for anything pinned to it |
| `data.json` | 1.4 kB stub so older builds can boot and notice an update |
| `scripts/normals.py` | monthly normals from the archive API |
| `scripts/serve_profile.py` | serves the profile over the LAN with the right MIME |
| `scripts/make_icons.py` | redraws the icon files, stdlib only |
| `.github/workflows/normals.yml` | manual, rebuilds `normals.json` |

## Local checks

```bash
python3 -m http.server 8765         # open http://127.0.0.1:8765
```

The page is tuned for 1024×768 in kiosk mode: everything fits without scrolling,
with 22 px of extra top padding for the translucent status bar.
