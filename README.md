# shawsuraj.com

Personal site of Suraj Shaw. Four worlds, one person.

Plain HTML, CSS and a little JavaScript. GSAP (from cdnjs) adds motion; the site works fully without it. No framework, no npm.

## Pages

- `index` Story: hero, Now board, four doors, five chapter story, the hospitality note.
- `guardian` Security, drawn as an assessment report.
- `builder` Products, drawn as a ship log.
- `researcher` Research, drawn as the first page of a paper.
- `human` Hospitality and elected roles, drawn as a bar menu and a ballot paper.

## Editing

1. Edit files in `src/`: `styles.css`, `app.js`, and `pages/*.html`. The first line of each page is its title, description and world.
2. Run `python3 build.py`. It writes the finished site to `dist/`.
3. Commit and push. Vercel serves `dist/` (set in `vercel.json`).

The nav, footer and contact links live once in `build.py`.

## Deploy on Vercel

1. Push this folder to a GitHub repo, for example `shawsuraj/shawsuraj.com`.
2. In Vercel: Add New, Project, import the repo. Framework preset: Other. Leave build settings as they are; `vercel.json` already points at `dist`.
3. Settings, Domains: add `shawsuraj.com` and `www.shawsuraj.com`, then add the DNS records Vercel shows at your registrar.
4. Keep your email DNS records (MX, SPF, DKIM) for shaw@shawsuraj.com untouched.

Short links: `/cv` (tech CV), `/tech`, `/bar`, `/research`.
