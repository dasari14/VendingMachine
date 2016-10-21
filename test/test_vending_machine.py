import pytest
from vending_machine.vending_machine import VendingMachine

# Function scoped to be more explicit with test state
@pytest.fixture(scope='function')
def vending_machine():
    vending_machine = VendingMachine()
    return vending_machine

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_accept_coin_nickle_returns_true(vending_machine):
        assert vending_machine.accept_coin('nickle') == True

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_accept_coin_coin_returns_false(vending_machine):
    assert vending_machine.accept_coin('coin') == False

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_accept_coin_nickle_adds_value(vending_machine):
    vending_machine.accept_coin('nickle')
    assert vending_machine.inserted_value() == 5

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_return_coins(vending_machine):
    vending_machine.accept_coin('nickle')
    coins = vending_machine.return_coins()
    assert coins == ['nickle']
    assert vending_machine.inserted_value() == 0

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_get_purchase_menu(vending_machine):
    menu = vending_machine.get_purchase_menu()
    assert menu == {'cola': 0, 'chips': 1, 'candy': 2}

@pytest.mark.usefixtures('vending_machine')
def test_vending_machine_purchase_chips_returns_nothing(vending_machine):
    button_to_press = vending_machine.get_purchase_menu()['chips']
    assert vending_machine.purchase(button_to_press) == []
