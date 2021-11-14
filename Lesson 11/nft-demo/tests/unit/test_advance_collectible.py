import pytest
from brownie import accounts, network
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link
from scripts.advanced_collectible.deploy import create_nft, deploy


def test_can_create_advance_collectible():
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip()
    account = get_account()
    advance_collectible=deploy(account)
    fund_with_link(advance_collectible.address)
    create_nft(advance_collectible,account)
    print("NFT OWNER"+ str(advance_collectible.ownerOf(0)))
    print("Expected owner: "+str(account))
    assert advance_collectible.ownerOf(0) == account
    assert advance_collectible.tokenIdToBreed(0) == 2
    pass
