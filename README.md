# Hire Me Holiday Parks — static HTML site

Plain HTML, CSS and JavaScript. No framework and no build step needed to run it:
open `index.html` in a browser, or upload the whole folder to any web host.

## Files
- `*.html` — 29 pages (see list below)
- `assets/styles.css` — all styling. Brand colours are the `--brand-*` / `--accent-*` variables at the top.
- `assets/main.js` — sticky header, mobile menu, form validation, job search and filters, alerts
- `assets/lucide.min.js` — icon library (local copy)
- `build.py` — optional. The header, footer and repeated content are generated from this one file,
  so a menu or footer change is made once and then `python3 build.py` rewrites every page.
  You can also just edit the HTML files directly and delete build.py.

## Pages
Home · Find a Job (search + filters) · Job detail (one per listing) · Job Seekers · Employers ·
Post a Job · Post a Resume · Services + 5 service pages · Resources + 5 guides · About · Contact ·
Login · Register · 404

## Before going live
1. Set the exact brand colours from the logo in `assets/styles.css`.
2. The logo and photos are loaded from hiremeholidayparks.com.au. Copy them into `assets/` and update the paths
   (in build.py: LOGO, HERO, SLIDES, IMG).
3. Listings with ids s1–s4 are samples. Job lists, counts and stats should come from the job board.
4. Forms validate in the browser only. Connect them to the server (see the TODO in main.js).
5. Add the business email and phone number in contact.html (marked with a comment).
