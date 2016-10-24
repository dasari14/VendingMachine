import pytest
from vending_machine.vending_machine import VendingMachine

# Function scoped to be more explicit with test state
@pytest.fixture(scope='function')
def vending_machine():
    vending_machine = VendingMachine()
    return vending_machine

def test_vending_machine_accept_coin_nickle_returns_true(vending_machine):
        assert vending_machine.accept_coin('nickle') == True

def test_vending_machine_accept_coin_coin_returns_false(vending_machine):
    assert vending_machine.accept_coin('coin') == False

def test_vending_machine_accept_coin_nickle_adds_value(vending_machine):
    vending_machine.accept_coin('nickle')
    assert vending_machine._inserted_value() == 5

def test_vending_machine_return_coins(vending_machine):
    vending_machine.accept_coin('nickle')
    vending_machine.return_coins()
    coins = vending_machine.empty_coin_return()
    assert coins == ['nickle']
    assert vending_machine._inserted_value() == 0

def test_vending_machine_get_purchase_menu(vending_machine):
    menu = vending_machine.get_purchase_menu()
    assert menu == {'cola': 0, 'chips': 1, 'candy': 2}

def test_vending_machine_purchase_chips_returns_nothing(vending_machine):
    button_to_press = vending_machine.get_purchase_menu()['chips']
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert chips_question_mark == []

def test_vending_machine_default_display(vending_machine):
    assert vending_machine.show_display() == 'INSERT COIN'

def test_vending_machine_display_purchase_chips_shows_price_then_insert_coin(vending_machine):
    button_to_press = vending_machine.get_purchase_menu()['chips']
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert vending_machine.show_display() == 'PRICE $0.50'
    assert vending_machine.show_display() == 'INSERT COIN'

def test_vending_machine_purchase_chips_returns_sold_out(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_purchase_menu()['chips']
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert chips_question_mark == []
    assert vending_machine.show_display() == 'SOLD OUT'

def test_vending_machine_accept_coin_changes_display_to_inserted_value(vending_machine):
    vending_machine.accept_coin('quarter')
    assert vending_machine.show_display() == '$0.25'

def test_vending_machine_reject_coin_goes_to_coin_return(vending_machine):
    vending_machine.accept_coin('coin')
    assert vending_machine.empty_coin_return() == ['coin']

def test_vending_machine_sold_out_display_goes_to_inserted_value(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_purchase_menu()['chips']
    vending_machine.select_product(button_to_press)
    vending_machine.show_display()
    assert vending_machine.show_display() == '$0.50'

def test_vending_machine_sold_out_display_no_money_goes_to_insert_coin(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_purchase_menu()['chips']
    vending_machine.select_product(button_to_press)
    vending_machine.return_coins()
    vending_machine.show_display()
    assert vending_machine.show_display() == 'INSERT COIN'

def test_vending_machine_return_coins_sets_display_to_insert_coin(vending_machine):
    vending_machine.accept_coin('quarter')
    assert vending_machine.show_display() == '$0.25'
    vending_machine.return_coins()
    assert vending_machine.show_display() == 'INSERT COIN'

def test_stock_vending_machine_adds_products(vending_machine):
    vending_machine._stock_vending_machine('chips', 1)
    assert vending_machine.inventory['chips'] == 1

def test_vending_machine_purchase_product_display_says_thank_you_then_reset(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_purchase_menu()['chips']
    vending_machine._stock_vending_machine('chips', 1)
    vending_machine.select_product(button_to_press)
    assert vending_machine.show_display() == 'THANK YOU'
    assert vending_machine.show_display() == 'INSERT COIN'

def test_vending_machine_returns_product_and_decreases_inventory(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_purchase_menu()['chips']
    vending_machine._stock_vending_machine('chips', 1)
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert chips_question_mark == ['chips']
    assert vending_machine.inventory['chips'] == 0
