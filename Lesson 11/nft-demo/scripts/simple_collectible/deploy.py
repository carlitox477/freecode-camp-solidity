from scripts.utils import get_account, OPENSEA_URL
from brownie import SimpleCollectible, config,network

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy(account):
    simple_collectible=SimpleCollectible.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
        )
    return simple_collectible

def create_nft(simple_collectible, account):
    print("Creating NFT")
    tx = simple_collectible.createCollectible(
        sample_token_uri,
        {"from": account}
        )
    tx.wait(1)
    print(f"Done, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address,simple_collectible.tokenCounter()-1)}")
    pass

def main():
    account = get_account()
    simple_collectible=deploy(account)
    create_nft(simple_collectible, account)
    pass