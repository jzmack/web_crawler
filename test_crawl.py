import unittest
from crawl import (
                normalize_url,
                get_heading_from_html,
                get_first_paragraph_from_html,
                get_urls_from_html,
                get_images_from_html,
                extract_page_data
                )

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

    def test_get_first_paragraph_main(self):
        input_body = '''<html><body>
                        <p>Outside paragraph.</p>
                        <main>
                            <p>Main paragraph.</p>
                        </main>
                        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_no_main(self):
        input_body ="""
                    <html><body>
                    <p>Outside paragraph.</p>
                    </body></html>
                    """
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)
    
    def test_no_p(self):
        input_body ="""
                    <html><body> Girl look at that body
                    </body></html>
                    """
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_html = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_html, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_html = '''
                    <html>
                      <body>
                        <a href="https://crawler-test.com">Go to Boot.dev</a>
                        <a href="https://example.com">Go to Example.com</a>
                      </body>
                    </html>
                    '''
        actual = get_urls_from_html(input_html, input_url)
        expected = ["https://crawler-test.com", "https://example.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_html = '''
                    <html>
                      <body>
                        <a href="https://crawler-test.com">Go to Boot.dev</a>
                        <a href="/blog">Blog</a>
                      </body>
                    </html>
                    '''
        actual = get_urls_from_html(input_html, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/blog"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body ='''<html>
                        <body>
                            <a href="https://crawler-test.com">Go to Boot.dev</a>
                            <img src="/logo.png" alt="Boot.dev Logo" />
                            <img src="/boots.png" alt="Boots image" />
                        </body>
                       </html>
                    '''
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/boots.png"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_none(self):
        input_url = "https://crawler-test.com"
        input_body ='''<html>
                        <body>
                            <a href="https://crawler-test.com">Go to Boot.dev</a>
                        </body>
                       </html>
                    '''
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_multiimage_nohead(self):
        input_url = "https://crawler-test.com"
        input_body ='''<html>
                        <body>
                            <p>This is the first paragraph.</p>
                            <a href="https://crawler-test.com">Go to Boot.dev</a>
                            <img src="/logo.png" alt="Boot.dev Logo" />
                            <img src="/boots.png" alt="Boots image" />
                        </body>
                       </html>
                    '''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com"],
            "image_urls": ["https://crawler-test.com/logo.png", "https://crawler-test.com/boots.png"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multilink_noparagraph(self):
        input_url = "https://crawler-test.com"
        input_body ='''<html>
                        <body>
                            <h1>Amazing heading</h1>
                            <a href="https://crawler-test.com">Go to Boot.dev</a>
                            <a href="/blog">Blog</a>
                            <img src="/logo.png" alt="Boot.dev Logo" />
                        </body>
                       </html>
                    '''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Amazing heading",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com", "https://crawler-test.com/blog"],
            "image_urls": ["https://crawler-test.com/logo.png"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_main_section(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <nav><p>Navigation paragraph</p></nav>
            <main>
                <h1>Main Title</h1>
                <p>Main paragraph content.</p>
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["heading"], "Main Title")
        self.assertEqual(actual["first_paragraph"], "Main paragraph content.")

    def test_extract_page_data_missing_elements(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = "<html><body><div>No h1, p, links, or images</div></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()