from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag

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
