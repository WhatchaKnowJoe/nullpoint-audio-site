# Null Point Audio — NP Vocal Suite

Website and release hosting for the NP Vocal Suite (NP-Zero, NP-Gate, NP-DeEss, NP-EQ, NP-Comp, NP-Verb, NP-Limit).

- `public/index.html` — the site (static, single file). Deployed by Vercel from `public/`.
- `build_site.py` — regenerates `public/index.html` from the SVG mockups in `design/`.
- `installer/` — NSIS script + license for the Windows installer.
- `thumbnails/` — plugin UI renders, dark and light.

The installer `.exe` lives in `public/downloads/` and is served by Vercel; the site's download button links to it.
