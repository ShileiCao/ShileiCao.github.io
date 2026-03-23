#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

def get_citation_count():
    url = "https://scholar.google.com/citations?hl=en&view_op=list_works&gmla=AJ1KiT3fCQn1gGUImjKvlxpSSYXWTtpQp3A_0EOaweuarUy4mgWOSjGIKOZAMb9dUfXPDnNM1Qf2o6tTpa3kpQ&user=-bCjtakAAAAJ"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for the citation count in the page
        # It might be in a div with class or id containing citation
        citation_text = soup.find(text=re.compile(r'Cited by \d+'))
        if citation_text:
            match = re.search(r'Cited by (\d+)', citation_text)
            if match:
                return match.group(1)

        # Alternative: look for specific elements
        # Sometimes it's in <a href="/citations?view_op=view_citation&...">Cited by XXX</a>
        citation_link = soup.find('a', href=re.compile(r'/citations\?view_op=view_citation'))
        if citation_link:
            match = re.search(r'Cited by (\d+)', citation_link.text)
            if match:
                return match.group(1)

        # If not found, try to find any element with "Cited by"
        elements = soup.find_all(text=re.compile(r'Cited by'))
        for elem in elements:
            match = re.search(r'Cited by (\d+)', str(elem))
            if match:
                return match.group(1)

        print("Citation count not found")
        return None

    except Exception as e:
        print(f"Error fetching citation count: {e}")
        return None

def update_html(citation_count):
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the placeholder
    new_content = re.sub(
        r'<span id="citation-count">Loading\.\.\.</span>',
        f'<span id="citation-count">{citation_count}</span>',
        content
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    citation_count = get_citation_count()
    if citation_count:
        update_html(citation_count)
        print(f"Updated citation count to {citation_count}")
    else:
        print("Failed to get citation count")