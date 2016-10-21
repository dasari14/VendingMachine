"""
@author: Logan Jewett

"""

from collections import defaultdict

class VendingMachine:

    default_coins = {
        "nickle": 5,
        "dime": 10,
        "quarter": 25
    }

    """
    Initialize this vending machine

    @param coins: coins is a dictionary input of string to integer mappings of
                  coins this vending machine will accept by name and their
                  associated values in cents.
    """
    def __init__(self, coins=default_coins):
        self.coins_accepted = coins
        self.inserted_coins = []
        self.register = defaultdict(int)

    """
    Attempt to insert a coin of NAME into the vending machine
    @param coin: coin is a string input representation of a coin that's being
                 inserted into the vending machine
    """
    def accept_coin(self, coin):
        if coin in self.coins_accepted.keys():
            self.inserted_coins.append(coin)
            return True
        else:
            return False

    def inserted_value(self):
        return sum(self.coins_accepted[coin] for coin in self.inserted_coins)

    def return_coins(self):
        coins_out = self.inserted_coins
        self.inserted_coins = []
        return coins_out
