from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, Tag
import requests
import asyncio
import aiohttp

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.max_concurrency = max_concurrency
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop is True:
                return False

            if normalized_url in self.page_data:
                return False

            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            return True

    async def get_html(self, url:str):
        async with self.session.get(
            url,
            headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if response.status >= 400:
                return None

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                print(f"Error: Not HTML content {content_type} for {url}")
                return None

            return await response.text()
    
    async def crawl_page(self, current_url):
        if self.should_stop is True:
            return

        parsed_current = urlparse(current_url)
        if self.base_domain != parsed_current.netloc:
            return

        normalized_url = normalize_url(current_url)
        first_time = await self.add_page_visit(normalized_url)
        if first_time is False:
            return

        try:
            async with self.semaphore:
                print(f"Crawling: {current_url} - (Active: {self.max_concurrency - self.semaphore._value})")
                current_html = await self.get_html(current_url)
                if current_html is None:
                    return
                page_info = extract_page_data(current_html, current_url)
                async with self.lock:
                    self.page_data[normalized_url] = page_info
                url_list = get_urls_from_html(current_html, self.base_url)
        except Exception as e:
            print(f"Error: {e}")
            return

        if self.should_stop:
            return

        tasks = [] 
        for url in url_list:
            task = asyncio.create_task(self.crawl_page(url))
            self.all_tasks.add(task)
            tasks.append(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task) 

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data 
    
async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()

# below is the old function, I'm keeping it here because it works
# but current version should be using the async functions
def crawl_page(base_url, current_url=None, page_data=None):
    if current_url == None:
        current_url = base_url

    if page_data == None:
        page_data = {}

    parsed_current = urlparse(current_url)
    parsed_base = urlparse(base_url)

    if parsed_current.netloc != parsed_base.netloc:
       return page_data 

    normalized_current = normalize_url(current_url)

    if normalized_current in page_data:
        return page_data
    
    print(f"Currently crawling: {current_url}")
    current_html = get_html(current_url)
    
    page_data[normalized_current] = extract_page_data(current_html, normalized_current)

    urls = get_urls_from_html(current_html, base_url)

    for url in urls:
        page_data = crawl_page(base_url, url, page_data)
    
    return page_data

# another function that works, replaced by async function
def get_html(url:str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"Error while connecting to URL: {e}")    
   
    if response.status_code >= 400:
        raise Exception(f"Error with client: {response.status_code}")
    
    content_type = response.headers.get("content-type")
    if content_type is None:
        content_type = ""
    if "text/html" not in content_type:
        raise Exception(f"Error incorrect header type: {response.headers.get('content-type')}")
   
    return response.text

def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    #print("URL=" + url)
    normalized_string = (parsed_url.netloc + parsed_url.path).rstrip("/").strip().lower()
    #print(normalized_string)
    return normalized_string 

def get_heading_from_html(html: str) -> str:
    html_doc = html
    soup = BeautifulSoup(html_doc, "html.parser")
    heading = soup.find("h1")
    if heading == None:
        heading = soup.find("h2")
        if heading == None:
            return ""
        return heading.get_text(strip=True)
    return heading.get_text(strip=True)

def get_first_paragraph_from_html(html: str) -> str:
    html_doc = html
    soup = BeautifulSoup(html_doc, "html.parser")
    main_sect = soup.find("main")
    if main_sect != None:
        first_p = main_sect.find("p")
        if first_p == None:
            return ""
        return first_p.get_text(strip=True)
    first_p = soup.find("p")
    if first_p == None:
        return ""
    return first_p.get_text(strip=True)

def get_urls_from_html(html: str, base_url:str) -> list[str]:
    html_doc = html
    soup = BeautifulSoup(html_doc, "html.parser")
    link_list = []
    if len(soup.find_all("a")) > 0:
        for link in soup.find_all("a"):
            parsed_link = link.get("href")
            link_list.append(urljoin(base_url, parsed_link))
    return link_list

def get_images_from_html(html:str , base_url:str) -> list[str]:
    html_doc = html
    soup = BeautifulSoup(html_doc, "html.parser")
    image_list = []
    if len(soup.find_all("img")) > 0:
        for image_link in soup.find_all("img"):
            parsed_link = image_link.get("src")
            image_list.append(urljoin(base_url, parsed_link))
    return image_list

def extract_page_data(html:str, page_url:str) -> dict:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }

