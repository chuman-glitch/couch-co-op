# Couch Co-Op

A public living room for play — pilot edition at POST Houston. An initiative by Nōvo Collective.

The site is a single-screen, spatial page: a collage of the room where each object opens a window.

## Layout

- `website/` — the static site (this folder is what gets published)
  - `index.html` — generated, don't edit by hand
  - `panels.js` — window logic, booking config (`CONFIG`), index order (`PANELS`)
  - `style.css` — window and booking styles
  - `concept/` — cut-outs (`lite/` is what the page loads), render footage, backdrop
  - `images/` — photos used inside the windows
- `tools/build_concept.py` — builds `website/index.html` (scene layout, labels, hover tips)
- `tools/windows.html` — the copy for every pop-up window

## Edit and rebuild

```bash
python3 tools/build_concept.py
python3 -m http.server 4321 --directory website
```

## Publish (GitHub Pages, `gh-pages` branch = the `website/` folder)

```bash
git subtree push --prefix website origin gh-pages
```

Domain: couchco-op.com (see `website/CNAME`).
