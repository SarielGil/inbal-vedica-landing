# Search indexing

Google Search Console: `sc-domain:vedica-ayurveda.co.il`.
Sitemap: `https://vedica-ayurveda.co.il/sitemap.xml`.

## Bing and IndexNow

`indexnow.json` points to a public verification text file in the site root.
This is an IndexNow ownership key, not a Bing account credential.

On a push to `main`, `.github/workflows/indexnow.yml` discovers changed public
HTML pages, including pages affected by changed assets or `content.json`.
Only pages in the current or previous sitemap are selected automatically;
templates, thank-you pages, private files and audit exports are excluded.
Renames notify both old and new paths. The homepage is submitted as `/`.

Before sending one POST to `https://api.indexnow.org/indexnow`, the script
checks that the live key and selected pages match the checked-out files.
Deleted pages must return 404 or 410. It waits up to ten minutes for hosting
to deploy. An expired wait or API error fails the workflow visibly.

Preview URLs from a newly published change:

```sh
python3 scripts/indexnow.py --since HEAD^ --dry-run
```

Retry after deployment, or run the workflow manually with the commit before
the changes:

```sh
python3 scripts/indexnow.py --since HEAD^ --wait-seconds 600
```

To notify one newly changed public page:

```sh
python3 scripts/indexnow.py --url https://vedica-ayurveda.co.il/clinic.html
```

Do not submit unchanged historical pages or schedule repeated bulk sitemap
notifications. HTTP 200 confirms receipt; 202 means ownership validation is
pending. Neither confirms crawling, indexing, ranking or Copilot citations.
Protocol reference: <https://www.indexnow.org/documentation>.

## Bing Webmaster Tools account

IndexNow works without connecting a Webmaster Tools account. To inspect
Bing indexing, queries, impressions and clicks, the site owner still needs
to sign in at <https://www.bing.com/webmasters/> and import Vedica from the
verified Google Search Console account (or select it if already imported).
Verify that the XML sitemap above is listed. The homepage itself is not an
XML sitemap. No Bing account verification tag is invented by this setup.

Import instructions:
<https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b>.
