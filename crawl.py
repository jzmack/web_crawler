from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, Tag
import requests

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
