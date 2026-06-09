import unittest
from crawl import normalize_url, get_heading_from_html

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_slash_at_end(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_spaces(self):
        input_url = "  https://www.boot.dev/blog/path   "
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_capitals(self):
        input_url = "https://www.BOOT.DEV/BLOG/PATH/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_get_head(self):
        input_html = """
                    <html>
                    <body>
                        <h1>Welcome to Boot.dev</h1>
                        <main>
                        <p>Learn to code by building real projects.</p>
                        <p>This is the second paragraph.</p>
                        </main>
                    </body>
                    </html>
                    """
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_from_h2(self):
        input_html = """
                    <html>
                    <body>
                        <h2>Welcome to Boot.dev</h2>
                        <main>
                        <p>Learn to code by building real projects.</p>
                        <p>This is the second paragraph.</p>
                        </main>
                    </body>
                    </html>
                    """
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_no_heading(self):
        input_html = """
                    <html>
                    <body>
                        <main>
                        <p>Learn to code by building real projects.</p>
                        <p>This is the second paragraph.</p>
                        </main>
                    </body>
                    </html>
                    """
        actual = get_heading_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()