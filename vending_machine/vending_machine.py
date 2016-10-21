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

        self.inserted_coins = []
        self.register = defaultdict(int)
        self.inventory = defaultdict(int)

    '''
    Attempt to insert a coin of NAME into the vending machine
    @param coin: coin is a string input representation of a coin that's being
                 inserted into the vending machine
    '''
    def accept_coin(self, coin):
        if coin in self.coins_accepted.keys():
            self.inserted_coins.append(coin)
            return True
        else:
            return False

    '''
    @return: The total value of inserted coins in cents
    '''
    def inserted_value(self):
        return sum(self.coins_accepted[coin] for coin in self.inserted_coins)

    '''
    @return: A list of all coins that have been inserted so far
    '''
    def return_coins(self):
        coins_out = self.inserted_coins
        self.inserted_coins = []
        return coins_out

    '''
    @return: A dictionary mapping item name to button number
    '''
    def get_purchase_menu(self):
        return dict(zip(
            [product['name'] for product in self.products],
            xrange(0, len(self.products))
        ))

    def purchase(self, button_number):
        return []
