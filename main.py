from crawl import crawl_site_async 
import sys
import asyncio

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    if len(sys.argv) == 2:
        base_url = sys.argv[1]
        print(f"starting crawl of: {base_url}")
    
    collected_pages = await crawl_site_async(base_url) 
    print(f"Crawler found {len(collected_pages)} total pages.")

    for page in collected_pages.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")

    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
