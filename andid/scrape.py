#! /usr/bin/env python3

import urllib.request
import os.path
import re
from bs4 import BeautifulSoup


BASE_URL = "http://www.andid.it"


def fetch_cached(path: str, cache_file: str) -> bytes:
    if os.path.isfile(cache_file):
        with open(cache_file, "rb") as f:
            return f.read()

    print(f"Fetch {path}")
    response = urllib.request.urlopen(f"{BASE_URL}{path}")
    html = response.read()

    print(f"Store {path}")
    with open(cache_file, "wb") as f:
        f.write(html)

    return html


def fetch_results_page(page: int) -> bytes:
    cache_file = f"data/results/{page}.html"
    path = f"/cerca-un-dietista/advanced-search/1012?page={page}"
    return fetch_cached(path, cache_file)


def fetch_item_page(path: str) -> bytes:
    item_name = path.split("/")[-1]
    cache_file = f"data/items/{item_name}.html"
    return fetch_cached(path, cache_file)


pages = 1
for page in range(1, pages + 1):
    print(f"Fetch page {page} of {pages}")
    html = fetch_results_page(page)

    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all(attrs={"class": "teaser-item"})

    print(f"Found {len(items)} items")

    for idx, item in enumerate(items[:10]):
        print(f"Fetch item {idx + 1} of {len(items)}")
        html = fetch_item_page(item.a["href"])

        soup = BeautifulSoup(html, "html.parser")
        item_data = soup.find(attrs={"class": "floatbox"})

        name = " ".join(
            n.capitalize() for n in item_data.find("h1").text.strip().split(" ")
        )
        print(f"Name: {name}")

        # debug
        # print(item_data)

        item_strings = [
            el.text for el in item_data.find_all(attrs={"class": "element"})
        ]
        phone = [s for s in item_strings if "Telefono" in s]
        if phone:
            phone_str = phone[0].strip()
            if phone_str.startswith("Telefono: "):
                phone_str = phone_str[len("Telefono: ") :]
        else:
            phone_str = "Missing"
        print(f"Phone: {phone_str}")

        address_element = item_data.find(attrs={"class": "pos-subtitle"})
        address = (
            re.sub("\s+", " ", address_element.text) if address_element else "Missing"
        )
        if address:
            address_str = address.strip()
            if address_str.startswith("Indirizzo: "):
                address_str = address_str[len("Indirizzo: ") :]
        else:
            address_str = "Missing"
        print(f"Address: {address_str}")

        metadata_container = item_data.find(attrs={"class": "pos-sidebar"})
        if metadata_container:
            metadata_els = metadata_container.find_all(attrs={"class": "element"})
            for metadata_el in metadata_els:
                metadata_title = metadata_el.find("h3").text.strip()
                metadata_content = metadata_el.text.strip()[len(metadata_title) :]
                print("Metadata")
                print(metadata_title, metadata_content.split(", "))
        else:
            print("Metadata: Missing")
