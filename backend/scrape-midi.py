import requests
from bs4 import BeautifulSoup
import os

CRAWL_DEPTH_LIMIT = 5
DOWNLOAD_LIMIT = 10


def download_file(url, destination):
    res = requests.get(url)
    if res.status_code == 200:
        url_parts = url.split("/")
        file_name = url_parts[-1]
        file_path = os.path.join(destination, f"{url_parts[-2]}-{file_name}")

        with open(file_path, "wb") as file:
            file.write(res.content)
        print(f"Downloading: {file_name}")
        return True
    else:
        print(f"Couldn't download: {url}")
        return False


def scrape_midi_page(url, destination):
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        anchor_els = soup.select("td > a")

        for anchor in anchor_els:
            href = anchor.get("href")
            if href and href.endswith('.mid'):
                download_file(href, destination)
    else:
        print(f"Failed to fetch: {url}")


def crawl_and_scrape_midi(url, download_destination, depth_counter, downloaded_count):
    if depth_counter >= CRAWL_DEPTH_LIMIT:
        return 0
    if downloaded_count >= DOWNLOAD_LIMIT:
        return 0

    _downloaded_count = 0
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        anchor_els = soup.select("td > a")

        for anchor in anchor_els:
            href = anchor.get("href")
            if href and href.endswith('.mid'):
                is_downloaded = download_file(href, download_destination)
                if is_downloaded:
                    _downloaded_count += 1
            elif href and depth_counter < CRAWL_DEPTH_LIMIT:
                print(f"Crawling on: {href}")
                new_counter = depth_counter + 1
                downloaded_from_new = crawl_and_scrape_midi(href,
                                                            download_destination,
                                                            new_counter,
                                                            downloaded_count+_downloaded_count)
                _downloaded_count += downloaded_from_new
    return _downloaded_count


if __name__ == "__main__":
    download_folder = "./data/game_midi"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    crawl_and_scrape_midi("https://www.khinsider.com/midi", download_folder, 0, 0)
