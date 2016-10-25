'''
@author: Logan Jewett

'''

from collections import defaultdict

class VendingMachine:

    '''
    Initialize this vending machine

    @param coins: coins is a dictionary input of string to integer mappings of
                  coins this vending machine will accept by name and their
                  associated values in cents.
    '''
    def __init__(self, coins, products):
        self.coins_accepted = coins
        self.products = products

        self.display = 'INSERT COIN'
        self.inserted_coins = []
        self._register = defaultdict(int)
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

    def _stock_vending_machine(self, product_name, product_count):
        self.inventory[product_name] += product_count

    def _refill_coin_register(self, coin_name, coin_count):
        self._register[coin_name] += coin_count

    def _get_coin_name(self, coin_value):
        for name, value in dict.iteritems(self.coins_accepted):
            if coin_value == value:
                return name

    def _make_change(self, change):
        minCoins = [0] * (change + 1)
        coinsUsed = [0] * (change + 1)
        for cents in range(change+1):

            coinCount = cents
            newCoin = 1
            for j in [c for c in self.coins_accepted.values() if c <= cents]:
                if minCoins[cents-j] + 1 < coinCount:
                    coinCount = minCoins[cents-j]+1
                    newCoin = j
            minCoins[cents] = coinCount
            coinsUsed[cents] = newCoin

        coins_returned = []
        coin = change
        while coin > 0:
            thisCoin = coinsUsed[coin]
            coin = coin - thisCoin
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
            [product['name'] for product in self.products],
            xrange(0, len(self.products))
        ))


    def select_product(self, button_number):
        product = self.products[button_number]
        inserted_value = self._inserted_value()
        if inserted_value < product['cost']:
            self.display = 'PRICE $%.2f' % (product['cost'] / 100.0)
        elif self.inventory[product['name']] == 0:
            self.display = 'SOLD OUT'
        else:
            self.display = 'THANK YOU'
            self.inventory[product['name']] -= 1
            change = self._make_change(inserted_value - product['cost'])
            self.coin_return = change
            self.inserted_value = []
            return [product['name']]
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
