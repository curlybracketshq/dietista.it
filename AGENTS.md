# Notes for coding agents (dietista.it)

Static Jekyll site for https://dietista.it, built and served by GitHub Pages.

## Branches and PRs — read this first

- `gh-pages` is the LIVE branch. `main` exists but is not what gets deployed.
  Every change to the site must target `gh-pages`, never `main`.
- Never push directly to `gh-pages`. Every change goes through a pull request:
  branch from `origin/gh-pages`, commit, push the branch, then
  `gh pr create --base gh-pages ...`
- Opening a PR against `main` (the `gh` default) is wrong and will be bounced.
- Commit style: lowercase `feat:` / `fix:` prefixes, e.g.
  `feat: add SaporePuro psyllium link to /links/`.

## Building / verifying

- There is no Gemfile, so no local `bundle exec jekyll build`. GitHub Pages
  builds the site on merge. Verify changes by inspection and with `curl`
  (e.g. thumbnail URLs must return HTTP 200), then test in prod after merge.

## /links/ page (`links/index.html`)

- Affiliate product buttons share one format — keep new entries identical:
  `a.link-btn.link-affiliate` (short `amzlink.to` href, `target="_blank"`,
  `rel="noopener sponsored nofollow"`) > `img.link-thumb` (76x76,
  `object-fit: contain` via page CSS) + `span` with the product title.
- The `links-note` disclosure paragraph below the buttons already covers all
  Amazon affiliate links; no per-link disclosure needed.
- Product thumbnails are VENDORED in `images/` (flat directory, descriptive
  lowercase names like `bucce-psillio-saporepuro.jpg`) and referenced as
  root-absolute `/images/...` paths. Never hotlink `m.media-amazon.com`.
