"""Checks for URL scope, deployment verification, and notification errors."""

import io
import unittest
import urllib.error
from contextlib import redirect_stdout
from unittest.mock import patch

import indexnow


HOST = "vedica-ayurveda.co.il"


class IndexNowTests(unittest.TestCase):
    def test_changed_pages_exclude_private_and_non_html(self):
        self.assertEqual(indexnow.select_urls(HOST, ["index.html", "clinic.html", "admin/a.html", "seo-logs/a.html", "thank-you.html", "blog-template.html", "sitemap.xml"]), ["https://" + HOST + "/", "https://" + HOST + "/clinic.html"])

    def test_removal_uses_previous_sitemap(self):
        self.assertEqual(indexnow.select_urls(HOST, ["old-page.html"], {"old-page.html"}), ["https://" + HOST + "/old-page.html"])

    def test_reject_other_origins_queries_and_paths(self):
        for url in ["https://example.com/clinic.html", "https://" + HOST + "/clinic.html?x=1", "http://" + HOST + "/", "https://" + HOST + "/../admin/a.html"]:
            with self.assertRaises(ValueError):
                indexnow.validate_url(HOST, url)

    def test_shared_styles_select_pages(self):
        urls = indexnow.select_urls(HOST, ["style.css"])
        self.assertIn("https://" + HOST + "/clinic.html", urls)
        self.assertIn("https://" + HOST + "/", urls)

    @patch("indexnow.urllib.request.urlopen")
    def test_stale_deployment_is_pending(self, open_url):
        response = open_url.return_value.__enter__.return_value
        response.geturl.return_value = "https://" + HOST + "/clinic.html"
        response.read.return_value = b"old page"
        url = "https://" + HOST + "/clinic.html"
        self.assertEqual(indexnow.deployment_ready({url: b"new page"}), [url])

    @patch("indexnow.urllib.request.urlopen")
    def test_deleted_page_requires_404_or_410(self, open_url):
        url = "https://" + HOST + "/removed.html"
        open_url.side_effect = urllib.error.HTTPError(url, 404, "missing", {}, None)
        self.assertEqual(indexnow.deployment_ready({url: None}), [])
        self.assertEqual(indexnow.deployment_ready({url: b"expected"}), [url])

    @patch("indexnow.urllib.request.urlopen")
    def test_live_bytes_and_final_url_must_match(self, open_url):
        url = "https://" + HOST + "/clinic.html"
        response = open_url.return_value.__enter__.return_value
        response.geturl.return_value = url
        response.read.return_value = b"page"
        self.assertEqual(indexnow.deployment_ready({url: b"page"}), [])
        response.geturl.return_value = "https://" + HOST + "/"
        self.assertEqual(indexnow.deployment_ready({url: b"page"}), [url])

    @patch("indexnow.deployment_ready", return_value=[])
    @patch("indexnow.urllib.request.urlopen")
    def test_accepted_is_reported_as_pending_key_validation(self, open_url, ready):
        response = open_url.return_value.__enter__.return_value
        response.status = 202
        response.read.return_value = b""
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(indexnow.main(["--url", "https://" + HOST + "/clinic.html"]), 0)
        self.assertIn("key validation pending", output.getvalue())

    @patch("indexnow.deployment_ready", return_value=[])
    @patch("indexnow.urllib.request.urlopen")
    def test_http_errors_fail(self, open_url, ready):
        open_url.side_effect = urllib.error.HTTPError(indexnow.ENDPOINT, 429, "limit", {}, io.BytesIO(b"Too many requests"))
        with self.assertRaisesRegex(RuntimeError, "HTTP 429"):
            indexnow.main(["--url", "https://" + HOST + "/clinic.html"])


if __name__ == "__main__":
    unittest.main()
