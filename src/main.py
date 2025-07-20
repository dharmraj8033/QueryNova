import argparse
import json
import csv
import sys
import asyncio
from modules.search import search
from modules.crawl import crawl_pages
from modules.ai_filter import rank_pages

def parse_args():
    parser = argparse.ArgumentParser(description="QueryNova CLI")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--csv", action="store_true", help="Output CSV")
    return parser.parse_args()

async def main():
    args = parse_args()
    results = search(args.query)
    urls = [r['link'] for r in results]
    pages = await crawl_pages(urls)
    ranked = rank_pages(args.query, pages)

    if args.json:
        print(json.dumps(ranked, indent=2))
    elif args.csv:
        writer = csv.writer(sys.stdout)
        writer.writerow(["url", "title", "summary", "score"])
        for item in ranked:
            writer.writerow([item["url"], item["title"], item["summary"], item["score"]])
    else:
        print("Ranked Results:")
        for item in ranked:
            print(f"{item['score']:.2f} {item['title']} - {item['url']}")
            print(item["summary"])
            print()

if __name__ == "__main__":
    asyncio.run(main())
