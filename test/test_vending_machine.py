'''
@author: Logan Jewett

'''

import pytest
from vending_machine.vending_machine import VendingMachine


default_coins = [
    {'coin_name': 'nickel', 'coin_value': 5, 'coin_count': 0},
    {'coin_name': 'dime', 'coin_value': 10, 'coin_count': 1},
    {'coin_name': 'quarter', 'coin_value': 25, 'coin_count': 0}
]

default_products = [
    {'product_name': 'cola', 'product_cost': 100},
    {'product_name': 'chips', 'product_cost': 50},
    {'product_name': 'candy', 'product_cost': 65}
]

# Function scoped to be more explicit with test state
@pytest.fixture(scope='function')
def vending_machine():
    vending_machine = VendingMachine(default_coins, default_products)
    return vending_machine

def test_accept_coin_nickel_returns_true(vending_machine):
        assert vending_machine.accept_coin('nickel') == True

def test_accept_coin_coin_returns_false(vending_machine):
    assert vending_machine.accept_coin('coin') == False

def test_accept_coin_nickel_adds_value(vending_machine):
    vending_machine.accept_coin('nickel')
    assert vending_machine._inserted_value() == 5

def test_return_coins(vending_machine):
    vending_machine.accept_coin('nickel')
    vending_machine.return_coins()
    coins = vending_machine.empty_coin_return()
    assert coins == ['nickel']
    assert vending_machine._inserted_value() == 0

def test_purchase_chips_returns_nothing(vending_machine):
    button_to_press = vending_machine.get_product_button('chips')
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert chips_question_mark == []

def test_default_display(vending_machine):
    assert vending_machine.show_display() == 'INSERT COIN'

def test_display_purchase_chips_shows_price_then_insert_coin(vending_machine):
    button_to_press = vending_machine.get_product_button('chips')
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert vending_machine.show_display() == 'PRICE $0.50'
    assert vending_machine.show_display() == 'INSERT COIN'

def test_purchase_chips_returns_sold_out(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('chips')
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert chips_question_mark == []
    assert vending_machine.show_display() == 'SOLD OUT'

def test_accept_coin_changes_display_to_inserted_value(vending_machine):
    vending_machine.accept_coin('quarter')
    assert vending_machine.show_display() == '$0.25'

def test_reject_coin_goes_to_coin_return(vending_machine):
    vending_machine.accept_coin('coin')
    assert vending_machine.empty_coin_return() == ['coin']

def test_sold_out_display_goes_to_inserted_value(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('chips')
    vending_machine.select_product(button_to_press)
    vending_machine.show_display()
    assert vending_machine.show_display() == '$0.50'

def test_sold_out_display_no_money_goes_to_insert_coin(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('chips')
    vending_machine.select_product(button_to_press)
    vending_machine.return_coins()
    vending_machine.show_display()
    assert vending_machine.show_display() == 'INSERT COIN'

def test_return_coins_sets_display_to_insert_coin(vending_machine):
    vending_machine.accept_coin('quarter')
    assert vending_machine.show_display() == '$0.25'
    vending_machine.return_coins()
    assert vending_machine.show_display() == 'INSERT COIN'

def test_stock_vending_machine_adds_products(vending_machine):
    slot_number = vending_machine.get_product_button('chips')
    vending_machine._stock_vending_machine(slot_number, 1)
    assert vending_machine.inventory[slot_number]['product_count'] == 1

def test_purchase_product_display_says_thank_you_then_reset(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('chips')
    vending_machine._stock_vending_machine(button_to_press, 1)
    vending_machine.select_product(button_to_press)
    assert vending_machine.show_display() == 'THANK YOU'
    assert vending_machine.show_display() == 'INSERT COIN'

def test_returns_product_and_decreases_inventory(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('chips')
    vending_machine._stock_vending_machine(button_to_press, 1)
    chips_question_mark = vending_machine.select_product(button_to_press)
    assert chips_question_mark == ['chips']
    assert vending_machine.inventory[button_to_press]['product_count'] == 0

def test_purchase_product_returns_change(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('candy')
    vending_machine._stock_vending_machine(button_to_press, 1)
    vending_machine.select_product(button_to_press)
    assert vending_machine.empty_coin_return() == ['dime']

def test_get_product_button_no_product_returns_neg_one(vending_machine):
    button_to_press = vending_machine.get_product_button('cheese')
    assert button_to_press == -1

def test_get_product_button_returns_candy_position(vending_machine):
    button_to_press = vending_machine.get_product_button('candy')

    # 0: cola
    # 1: chips
    # 2: candy
    assert button_to_press == 2

def test_stock_new_product(vending_machine):
    vending_machine._stock_vending_machine(
        4,
        {'product_name': 'cheese', 'product_cost': 150, 'product_count': 1}
    )

    button_to_press = vending_machine.get_product_button('cheese')
    assert button_to_press == 4

def test_get_product_button_returns_candy_slot(vending_machine):

    vending_machine._stock_vending_machine(
        4,
        {'product_name': 'candy', 'product_cost': 65, 'product_count': 1}
    )

    # 0: cola
    # 1: chips
    # 2: candy <- this candy slot is empty
    # 3: nothing
    # 4: candy <- return this

    candy_location = vending_machine.get_product_button('candy')
    assert candy_location == 4

def test_default_message_no_coins_exact_change_only(vending_machine):
    vending_machine._refill_coin_register('dime', -1)
    assert vending_machine.show_display() == 'EXACT CHANGE ONLY'

def test_default_message_switch_when_coin_added(vending_machine):
    vending_machine._refill_coin_register('dime', -1)
    assert vending_machine.show_display() == 'EXACT CHANGE ONLY'
    vending_machine._refill_coin_register('dime', 1)
    assert vending_machine.show_display() == 'INSERT COIN'

def test_purchasing_products_and_making_change_changes_coins_in_register(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('candy')
    vending_machine._stock_vending_machine(button_to_press, 1)
    vending_machine.select_product(button_to_press)
    assert vending_machine._register['dime'] == 0
    assert vending_machine._register['quarter'] == 3

def test_make_change_returns_sub_optimal_change(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('candy')
    vending_machine._stock_vending_machine(button_to_press, 1)
    vending_machine._refill_coin_register('dime', -1)
    vending_machine._refill_coin_register('nickel', 2)
    vending_machine.select_product(button_to_press)
    assert vending_machine.empty_coin_return().count('nickel') == 2

def test_unable_to_make_change(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('candy')
    vending_machine._stock_vending_machine(button_to_press, 1)
    vending_machine._refill_coin_register('dime', -1)
    vending_machine.select_product(button_to_press)
    assert vending_machine.show_display() == 'UNABLE TO MAKE CHANGE'

def test_unable_to_make_change_with_some_coins_still_available(vending_machine):
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    vending_machine.accept_coin('quarter')
    button_to_press = vending_machine.get_product_button('candy')
    vending_machine._stock_vending_machine(button_to_press, 1)
    vending_machine._refill_coin_register('dime', -1)
    vending_machine._refill_coin_register('quarter', 1)
    vending_machine._refill_coin_register('nickel', 1)
    vending_machine.select_product(button_to_press)
    assert vending_machine.show_display() == 'UNABLE TO MAKE CHANGE'
