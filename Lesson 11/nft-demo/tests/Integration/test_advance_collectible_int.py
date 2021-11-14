import pytest
from brownie import network
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link
from scripts.advanced_collectible.deploy import create_nft, deploy
import time


def test_can_create_advance_collectible_int():
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        pytest.skip()
        pass
    account = get_account()
    advance_collectible=deploy(account)
    fund_with_link(advance_collectible.address)
    create_nft(advance_collectible,account)
    time.sleep(120)
    assert advance_collectible.ownerOf(0) == account
    pass
