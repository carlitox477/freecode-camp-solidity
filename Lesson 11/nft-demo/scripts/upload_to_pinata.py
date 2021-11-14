import os
from pathlib import Path

import requests
from requests.api import head
PINATA_BASE_URL="https://api.pinata.cloud/"
PIN_FILE_ENDPOINT="pinning/pinFileToIPFS"
FILE_FOLDER="./img/"
HEADERS={"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_API_SECRET")}
IMAGE_URI="https://ipfs.io/ipfs/{}?filename={}"

def upload_to_pinata(filepath,file_name):
    print(filepath)
    image_uri="Couldn't upload "+file_name
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response= requests.post(
            PINATA_BASE_URL+PIN_FILE_ENDPOINT,
            files={"file": (file_name,image_binary)},
            headers=HEADERS
            )
        response_json=response.json()
        print(response_json)
        image_uri=IMAGE_URI.format(response_json["IpfsHash"],file_name)
        pass
    return image_uri


def main():
    file_name="pug.png"
    filepath=FILE_FOLDER+file_name
    image_uri=upload_to_pinata(filepath,file_name)
    print(image_uri)
    pass