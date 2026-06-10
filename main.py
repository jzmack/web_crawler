from crawl import crawl_site_async 
import sys
import asyncio

async def main():
    if len(sys.argv) < 4:
        print("not enough arguments provided")
        print("usage:")
        print("uv run main.py URL max_concurrency max_pages")
        print("example:")
        print("uv run main.py https://crawler-test.com/ 3 25")
        sys.exit(1)

    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    if len(sys.argv) == 4:
        base_url = sys.argv[1]
        max_concurrency = int(sys.argv[2])
        max_pages = int(sys.argv[3])
        print(f"starting crawl of: {base_url} with a concurrency of {max_concurrency} and max of {max_pages} pages")
    
    collected_pages = await crawl_site_async(base_url, max_concurrency, max_pages) 
    print(f"Crawler found {len(collected_pages)} total pages.")

    for page in collected_pages.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
