import os
from typing import Dict
import requests
import re
import html
from tabulate import tabulate
import argparse

__version__ = "1.0.1"

url = "https://www.zupimages.net/up.php"
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

latest_version_url = "https://raw.githubusercontent.com/PhunkyBob/zupimages/master/VERSION"
latest_binary = "https://github.com/PhunkyBob/zupimages/releases/latest"
git_repo = "https://github.com/PhunkyBob/zupimages"


def check_version(version: str) -> str:
    latest_version = ""
    res = requests.get(latest_version_url)
    if res.status_code != 200:
        print(f"Version {version} (can't check official version)")
    else:
        latest_version = res.text.strip()
        if latest_version == version:
            print(f"Version {version} (official version)")
        else:
            print(f"Version {version} (official version is different: {latest_version})")
            print(f"Please check {latest_binary}")
    print()
    return latest_version


def remove_html_tags(text: str) -> str:
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text).strip()


def upload_file(url: str, file_path: str) -> str:
    headers = {
        "authority": "www.zupimages.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "origin": "https://www.zupimages.net",
        "pragma": "no-cache",
        "referer": "https://www.zupimages.net/api/index.php?background=transparent&color=000000&header=yes&lastimage=yes",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": user_agent,
    }

    params = {
        "background": "transparent",
        "color": "000000",
        "header": "yes",
        "lastimage": "yes",
    }

    with open(file_path, "rb") as file:
        files = {"files[]": file}
        response = requests.post(url, params=params, headers=headers, files=files)
        if response.status_code != 200:
            print(f"Error: {response.status_code} -> {response.reason}")
            return ""
        return response.text


def parse_response(content: str) -> Dict[str, str]:
    if res := re.findall(r'<strong>(.+)?:(.+)?<input class="all-select" type="text" value="(.+)?"', content):
        return {remove_html_tags(elem[0]): html.unescape(elem[-1]) for elem in res}

    return {}


def is_image(file_path: str) -> bool:
    return os.path.splitext(file_path)[-1].lower() in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif"]


pause_before_exit = False


def before_exit():
    if pause_before_exit:
        input("\nPress [Enter] to exit...")


def main() -> None:
    global pause_before_exit
    print(f"zupimages - {git_repo}")
    # check_version(__version__)
    parser = argparse.ArgumentParser(
        description=f'Script to upload a file to "zupimages.net".\nSource: {git_repo}',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("file", type=str, nargs="?", help="Path to the image file to upload.")
    args = parser.parse_args()
    file_path = args.file
    if not file_path:
        file_path = input("Enter the path to the image file to upload: ")
        pause_before_exit = True

    if not os.path.exists(file_path):
        print(f'Error: File "{file_path}" does not exist...')
        before_exit()
        return
    if not is_image(file_path):
        print(f'Error: File "{file_path}" is not an image...')
        before_exit()
        return
    response_content = upload_file(url, file_path)
    if not response_content:
        before_exit()
        return
    links = parse_response(response_content)
    if not links:
        print("Error: No link found...")
        before_exit()
        return
    list_values = list(links.items())
    print(tabulate(list_values, tablefmt="rounded_grid"))
    before_exit()


if __name__ == "__main__":
    main()
