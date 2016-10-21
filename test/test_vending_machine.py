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

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_accept_coin_nickle_adds_value(vending_machine):
    vending_machine.accept_coin("nickle")
    assert vending_machine.inserted_value() == 5

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_return_coins(vending_machine):
    vending_machine.accept_coin('nickle')
    coins = vending_machine.return_coins()
    assert coins == ['nickle']
    assert vending_machine.inserted_value() == 0
