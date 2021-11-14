from brownie import network, AdvanceCollectible
from scripts.utils import get_breed,get_account, OPENSEA_URL

DOG_METADATA = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id,tokenURI, {"from": account})
    tx.wait(1)
    print(f"Success: you can view your NFT at {OPENSEA_URL.format(nft_contract.address,token_id)}")
    print("You may need to wait up to 20 minutes to see the nft on opensea")
    pass

def main():
    print(f"Working on {network.show_active()}")
    advance_collectible=AdvanceCollectible[-1]
    total_collectibles= advance_collectible.tokenCounter()
    print(f"There are {total_collectibles} tokens ids")
    for token_id in range(0, total_collectibles):
        breed=get_breed(advance_collectible.tokenIdToBreed(token_id))
        metadata=DOG_METADATA[breed]
        if (not advance_collectible.tokenURI(token_id).startswith("https//")):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id,advance_collectible,metadata)
        pass