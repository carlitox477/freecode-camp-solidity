from scripts.utils import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS
    )
from brownie import AdvanceCollectible, config,network, Contract,VRFCoordinatorMock


sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy(account):
    vrf_coordinator =get_contract("vrf_coordinator")
    link_token = get_contract("link_token")

    print("Deploying AdvanceCollectible")
    advance_collectible=AdvanceCollectible.deploy(
        vrf_coordinator.address,
        link_token.address,
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
        )
    print("AdvanceCollectible deployed")
    return advance_collectible

def create_nft(advance_collectible, account):
    print("Creating NFT")
    create_tx = advance_collectible.createCollectible(
        {"from": account}
        )
    create_tx.wait(1)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        vrf_coordinator = VRFCoordinatorMock[-1]
        request_id=create_tx.events["RequestCollectible"]["requestId"]
        print("Request id "+str(request_id))
        tx_callback = vrf_coordinator.callBackWithRandomness(
            request_id,
            2,
            advance_collectible.address,
            {"form": account})
        tx_callback.wait(1)
        print(f"Done, NFT created")
    else:
        print(f"Done, you can view your NFT at {OPENSEA_URL.format(advance_collectible.address,advance_collectible.tokenCounter()-1)}")
        pass
    
    pass

def main():
    account = get_account()
    #advance_collectible=deploy(account)
    
    if(len(AdvanceCollectible)<=0):
        advance_collectible=deploy(account)
    else:
        advance_collectible= AdvanceCollectible[-1]
        pass
    
    fund_with_link(
        advance_collectible.address,
        amount=config["networks"][network.show_active()]["fee"]
        )

    create_nft(advance_collectible, account)
    pass