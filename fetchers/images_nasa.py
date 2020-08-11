"""
Download images using NASA's image API. Current implementation does not return video or audio results.
API docs: https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf
Run the script from the project directory.

You must include two command line arguments:
- `searchterm`: what term you want to search the NASA image API for
- `imagedir`: what directory you want to save them in, which you have already created inside the data directory. For example, I have created `./data/nasa-sun`
and so I use `imagedir=nasa-sun`.

Keep in mind some search terms can return > 50 pages of results and thousands of images.

TODO:
- handle errors in `download_image` function
"""

import argparse
import requests
from urllib.request import urlretrieve

API_ROOT_URL = "https://images-api.nasa.gov"
IMAGE_DIR_PATH = "./data/{dirname}/"

def request_images(api_url):
    """
    Request a page of results from the image API given a URL,
    download images from that page,
    and return the provided URL to fetch the next page of results.
    """
    response = requests.get(api_url)
    collection = response.json()["collection"]

    for asset in collection["items"]:
        image_link = asset['links'][0]['href'] # grabs thumbnail
        download_image(args.image_dir, image_link)

    next_url = None
    links = collection['links']
    for link in links:
        if link['rel'] == "next":
            next_url = link['href']
    return next_url

def download_image(image_dir, image_link):
    """
    Download an image to the specified image directory,
    given the link to that image.
    """
    download_dir = IMAGE_DIR_PATH.format(dirname=image_dir)
    image_fname = image_link.split('/')[-1]
    download_path = download_dir + str(image_fname)
    urlretrieve(image_link, download_path)
    return

def main(args):
    """
    Iterate through API pages until we're done finding and saving the images
    associated with our search term.
    """

    if not args.search_term:
        print("Search term is required for this implementation")
        return 1

    if not args.image_dir:
        print("Please specify a directory (of data dir) to store the images.")
        return 1

    api_url = API_ROOT_URL + "/search?q={q}&media_type=image".format(q=args.search_term)

    while api_url is not None:
        print(api_url)
        api_url = request_images(api_url)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--searchterm",
        dest="search_term",
        type=str,
        default=None,
        help="limit results fetched from API to those matching search term.")
    parser.add_argument(
        "--imagedir",
        dest="image_dir",
        type=str,
        default=None,
        help="specify a directory name to save your images in (you must create it before running)."
    )
    args = parser.parse_args()
    main(args)
