"""
fetch_competitor_specs.py
Helper script to fetch public Amazon product specifications (Page count, Dimensions, Publisher)
for our benchmark ASINs.

Note: Amazon frequently serves CAPTCHAs or 503s to automated scripts. If blocked,
the script outputs direct manual links for quick inspection.
"""

import urllib.request
import re
import json
import time

ASINS = {
    "1454961791": "Murdoku: 80 Murder Mystery Logic Puzzles",
    "0316616184": "The Killer Isn't Alice",
    "1250892317": "Murdle: Volume 1"
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_details(html_text):
    results = {}
    
    # Check for CAPTCHA
    if "api-services-support@amazon.com" in html_text or "Type the characters you see in this image" in html_text:
        return {"error": "CAPTCHA / Bot detection triggered"}

    # Extract Print Length / Page count
    pages_match = re.search(r'(\d+)\s+pages', html_text, re.IGNORECASE)
    if pages_match:
        results["pages"] = f"{pages_match.group(1)} pages"
    else:
        # Check carousel / detail bullets
        detail_match = re.search(r'Print length[^<]*</span>[^<]*<span>(\d+)\s*pages', html_text, re.IGNORECASE)
        if detail_match:
            results["pages"] = f"{detail_match.group(1)} pages"

    # Extract Dimensions
    dim_match = re.search(r'Dimensions[^<]*</span>[^<]*<span>([^<]+)</span>', html_text, re.IGNORECASE)
    if dim_match:
        results["dimensions"] = dim_match.group(1).strip()
    else:
        # Fallback regex for standard dimension strings like "6 x 0.5 x 9 inches"
        dim_generic = re.search(r'(\d+(?:\.\d+)?\s*x\s*\d+(?:\.\d+)?\s*x\s*\d+(?:\.\d+)?\s*inches)', html_text, re.IGNORECASE)
        if dim_generic:
            results["dimensions"] = dim_generic.group(1).strip()

    # Extract Publisher
    pub_match = re.search(r'Publisher[^<]*</span>[^<]*<span>([^<]+)</span>', html_text, re.IGNORECASE)
    if pub_match:
        results["publisher"] = pub_match.group(1).strip()

    return results

def main():
    print("=" * 60)
    print("AMAZON COMPETITOR SPECIFICATION LOOKUP")
    print("=" * 60)
    
    collected_data = {}

    for asin, title in ASINS.items():
        url = f"https://www.amazon.com/dp/{asin}"
        print(f"\nChecking ASIN {asin} ({title})...")
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                details = extract_details(html)
                if "error" in details:
                    print(f"  [!] {details['error']}")
                    print(f"  [>] Manual link: {url}")
                else:
                    print(f"  [+] Pages: {details.get('pages', 'Not found')}")
                    print(f"  [+] Dimensions: {details.get('dimensions', 'Not found')}")
                    print(f"  [+] Publisher: {details.get('publisher', 'Not found')}")
                    collected_data[asin] = details
        except Exception as e:
            print(f"  [!] Request failed ({e}).")
            print(f"  [>] Manual link: {url}")
        
        time.sleep(1.5)

    with open("competitor_specs.json", "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=2)
    print("\nSaved output to competitor_specs.json")

if __name__ == "__main__":
    main()
