'''
@author: Logan Jewett

'''
import sys
from collections import defaultdict

class VendingMachine:

    '''
    Initialize this vending machine

    @param coins: coins is a list of dictionaries of coin_name to coin_value (in cents) mappings
                  Optionally may include a coin_count parameter that indicates how many of that type
                  of coin to insert. Defaults to 0
                  e.g. [
                           {'coin_name': 'quarter', 'coin_value': 25, 'coin_count': 10},
                           {'coin_name': 'dime', 'coin_value': 10},
                           {'coin_name': 'nickle', 'coin_value': 5}
                       ]

    @param products: products is a list of dictionaries of product_name to product_cost (in cents) mappings
                     Optionally may include a product_count parameter that indicates how many of that type
                     of product to insert. Defaults to 0
                     e.g. [
                              {'product_name': 'chips', 'product_cost': 100, 'product_count': 3},
                              {'product_name': 'soda', 'product_cost': 50},
                              {'product_name': 'candy', 'product_cost': 65}
                          ]
    '''
    def __init__(self, coins, products):
        self._coin_name_to_value_map = dict()
        self._register = defaultdict(int) # Internal Coin Storage

        for coin in coins:
            self._add_accepted_coin(coin)

        self.inventory = products
        for product in self.inventory:
            if not product.has_key('product_count'):
                product['product_count'] = 0

        self.display = 'INSERT COIN' # Physical Display
        self.inserted_coins = list() # P

        self.coin_return = list() # Physical Coin Return

    '''
    Attempt to insert a coin of COIN_NAME into the vending machine
    @param coin: coin is a string input representation of a coin that's being
                 inserted into the vending machine
    '''
    def accept_coin(self, coin_name):
        if self._check_coin_accepted(coin_name):
            self.inserted_coins.append(coin_name)
            self.display = '$%.2f' % (self._inserted_value() / 100.0)
            return True
        else:
            self.coin_return.append(coin_name)
            self.display = 'INSERT COIN'
            return False

    '''
    @return: The total value of inserted coins in cents
    '''
    def _inserted_value(self):
        return sum(self._coin_name_to_value_map[coin] for coin in self.inserted_coins)

    def _stock_vending_machine(self, slot_number, product_count):
        self.inventory[slot_number]['product_count'] = product_count

    def _refill_coin_register(self, coin_name, coin_count):
        self._register[coin_name] += coin_count

    def _get_coin_name(self, coin_value):
        for name, value in dict.iteritems(self._coin_name_to_value_map):
            if coin_value == value:
                return name
        return None

    def _check_coin_accepted(self, coin_name):
        return self._coin_name_to_value_map.has_key(coin_name)

    def _add_accepted_coin(self, coin):
        if not self._check_coin_accepted(coin['coin_name']) and\
                self._get_coin_name(coin['coin_value']) == None:

            self._coin_name_to_value_map[coin['coin_name']] = coin['coin_value']
            self._register[coin['coin_name']] = coin.get('coin_count', 0)
    # def _coins_available(self):
    #     coins_available = []
    #     for coin_name, coin_count in dict.iteritems(self._register):
    #         if coin_count > 0:
    #             coins_available.append(self._coin_name_to_value_map[coin_name])
    #     return coins_available

    def _make_change(self, change_to_make):
        minCoins = [0] * (change_to_make + 1)
        coinsUsed = [0] * (change_to_make + 1)
        for cents in range(change_to_make + 1):

            coinCount = cents
            newCoin = 1
            for j in [c for c in self._coin_name_to_value_map.values() if c <= cents]:
                if minCoins[cents-j] + 1 < coinCount:
                    coinCount = minCoins[cents-j]+1
                    newCoin = j
            minCoins[cents] = coinCount
            coinsUsed[cents] = newCoin

        coins_returned = []
        change_left_to_make = change_to_make
        while change_left_to_make > 0:
            thisCoin = coinsUsed[change_left_to_make]
            change_left_to_make -= thisCoin
            coins_returned.append(self._get_coin_name(thisCoin))
        return coins_returned


    def return_coins(self):
        self.coin_return += self.inserted_coins
        self.inserted_coins = []
        self.display = 'INSERT COIN'


    def empty_coin_return(self):
        coins_out = self.coin_return
        self.coin_return = []
        return coins_out


    '''
    @return: A dictionary mapping item name to button number
    '''
    def get_purchase_menu(self):
        return dict(zip(
            [product['product_name'] for product in self.inventory],
            xrange(0, len(self.inventory))
        ))


    def select_product(self, button_number):
        product = self.inventory[button_number]
        inserted_value = self._inserted_value()
        if inserted_value < product['product_cost']:
            self.display = 'PRICE $%.2f' % (product['product_cost'] / 100.0)
        elif product['product_count'] == 0:
            self.display = 'SOLD OUT'
        else:
            self.display = 'THANK YOU'
            product['product_count'] -= 1
            change = self._make_change(inserted_value - product['product_cost'])
            self.coin_return = change
            self.inserted_value = []
            return [product['product_name']]
        return []


    def show_display(self):
        display = self.display
        if self.display.startswith('PRICE'):
            self.display = 'INSERT COIN'
        elif self.display.startswith('SOLD OUT'):
            current_value = self._inserted_value()
            self.display = '$%.2f' % (current_value / 100.0) if current_value else 'INSERT COIN'
        elif self.display.startswith('THANK YOU'):
            self.display = 'INSERT COIN'
        return display
