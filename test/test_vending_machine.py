import pytest
from vending_machine.vending_machine import VendingMachine

@pytest.fixture
def vending_machine(scope='session'):
    vending_machine = VendingMachine()
    return vending_machine

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_accept_coin_nickle_returns_true(vending_machine):
        assert vending_machine.accept_coin("nickle") == True

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_accept_coin_coin_returns_false(vending_machine):
    assert vending_machine.accept_coin("coin") == False
