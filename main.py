from crawl import crawl_page 
import sys

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    if len(sys.argv) == 2:
        base_url = sys.argv[1]
        print(f"starting crawl of: {base_url}")
    
    collected_pages = crawl_page(base_url)
    print(f"Crawler found {len(collected_pages)} pages.")

    for url, data in collected_pages.items():
        print(f"URL: {url}")
        print(f"Heading: {data['heading']}")

    sys.exit(0)

if __name__ == "__main__":
    main()
