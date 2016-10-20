import pytest
from vending_machine.vending_machine import VendingMachine

def test_vending_machine_accept_coin_nickle_returns_true():
    vending_machine = VendingMachine()
    assert vending_machine.accept_coin("nickle") == True
