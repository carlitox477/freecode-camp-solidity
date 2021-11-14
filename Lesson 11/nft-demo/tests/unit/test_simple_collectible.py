import pytest
from brownie import accounts, network
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.simple_collectible.deploy import create_nft, deploy


def test_can_create_simple_collectible():
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip()
    account = get_account()
    simple_collectible=deploy(account)
    create_nft(simple_collectible,account)
    #print("NFT OWNER"+ str(simple_collectible.ownerOf(0)))
    #print("Expected owner: "+str(account))
    assert simple_collectible.ownerOf(0) == account
    pass
