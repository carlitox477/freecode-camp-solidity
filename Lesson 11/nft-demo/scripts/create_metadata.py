
import json
from pathlib import Path
from brownie import AdvanceCollectible,network
from scripts.utils import get_breed
from scripts.upload_to_pinata import upload_to_pinata
from metadata.sample_metadata import meta_template
import requests
import os

sample_uri="https://ipfs.io/ipfs/{}?filename={}"

BREED_TO_IMAGE_URI={
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png"
    }

def upload_to_ipfs(filepath):
    result=None
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url= "http://127.0.0.1:5001"
        end_point="/api/v0/add"
        response = requests.post(ipfs_url+end_point, files={"file": image_binary})
        json_response = response.json()
        print(json_response)
        ipfs_hash=json_response["Hash"]
        filename=filepath.split("/")[-1:][0]
        image_uri=f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        result= image_uri
        pass
    return result

def main():
    advance_collectible=AdvanceCollectible[-1]
    total_advanced_collectibles=advance_collectible.tokenCounter()
    print(f"You have created {total_advanced_collectibles} collectibles")
    
    for token_id in range(0,total_advanced_collectibles):
        breed = get_breed(advance_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(metadata_file_name)
        
        collectible_metadata = meta_template
        
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} alredy exists! Delete it to overwrite")
        else:
            print(f"Creating metdata file: {metadata_file_name}")
            collectible_metadata["name"]=breed
            collectible_metadata["description"]=f"An addorable {breed} pup"
            
            image_file_name= "./img/"+breed.lower().replace("_","-")+".png"
            
            image_uri=None
            
            if (os.getenv("UPLOAD_IPFS")==True):
                image_uri=upload_to_ipfs(image_file_name)
                pass
            image_uri = image_uri if image_uri else BREED_TO_IMAGE_URI[breed]
            
            collectible_metadata["image_uri"]=image_uri
            with open(metadata_file_name, "w") as file:
                #It save a dictionary on a file
                json.dump(collectible_metadata, file)
                pass
            
            if (os.getenv("UPLOAD_IPFS")==True):
                upload_to_ipfs(metadata_file_name)
                pass
            
            
            print(collectible_metadata)
            pass
        pass
        
    pass