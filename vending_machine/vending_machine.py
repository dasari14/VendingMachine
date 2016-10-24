'''
@author: Logan Jewett

'''

from collections import defaultdict

class VendingMachine:

    default_coins = {
        'nickle': 5,
        'dime': 10,
        'quarter': 25
    }

    default_products = [
        {'name': 'cola', 'cost': 100},
        {'name': 'chips', 'cost': 50},
        {'name': 'candy', 'cost': 65}
    ]

    '''
    Initialize this vending machine

    @param coins: coins is a dictionary input of string to integer mappings of
                  coins this vending machine will accept by name and their
                  associated values in cents.
    '''
    def __init__(self, coins=default_coins, products=default_products):
        self.coins_accepted = coins
        self.products = products

        self.display = 'INSERT COIN'
        self.inserted_coins = []
        self.register = defaultdict(int)
        self.inventory = defaultdict(int)
        self.coin_return = []

    '''
    Attempt to insert a coin of NAME into the vending machine
    @param coin: coin is a string input representation of a coin that's being
                 inserted into the vending machine
    '''
    def accept_coin(self, coin):
        if coin in self.coins_accepted.keys():
            self.inserted_coins.append(coin)
            self.display = '$%.2f' % (self._inserted_value() / 100.0)
            return True
        else:
            self.coin_return.append(coin)
            self.display = 'INSERT COIN'
            return False

    '''
    @return: The total value of inserted coins in cents
    '''
    def _inserted_value(self):
        return sum(self.coins_accepted[coin] for coin in self.inserted_coins)


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
            [product['name'] for product in self.products],
            xrange(0, len(self.products))
        ))


    def select_product(self, button_number):
        product = self.products[button_number]
        if self._inserted_value() < product['cost']:
            self.display = 'PRICE $%.2f' % (product['cost'] / 100.0)
        elif self.inventory[product['name']] == 0:
            self.display = 'SOLD OUT'
        return []


    def show_display(self):
        display = self.display
        if self.display.startswith('PRICE'):
            self.display = 'INSERT COIN'
        elif self.display.startswith('SOLD OUT'):
            current_value = self._inserted_value()
            self.display = '$%.2f' % (current_value / 100.0) if current_value else 'INSERT COIN'
        return display
