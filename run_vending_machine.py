#!/usr/bin/env python
'''
@author: Logan Jewett

'''

import json
import argparse
from tabulate import tabulate
from vending_machine.vending_machine import VendingMachine

def main():
    '''
    The main program loop for the Vending Machine program
    '''
    parser = argparse.ArgumentParser(
        description='A CLI Vending Machine. After running type help for more commands'
    )

    parser.add_argument(
        'coins_file',
        type=argparse.FileType('r'),
        nargs='?',
        default=open('./vending_machine/coins.json', 'r'),
        help='Location for the JSON file of initial coin definitions'
    )

    parser.add_argument(
        'products_file',
        type=argparse.FileType('r'),
        nargs='?',
        default=open('./vending_machine/products.json', 'r'),
        help='Location for the JSON file of initial product definitions'
    )

    cli_args = parser.parse_args()

    vending_machine = VendingMachine(
        json.load(cli_args.coins_file), json.load(cli_args.products_file)
    )

    commands = {
        'insert': 'accept_coin',
        'return': 'return_coins',
        'empty': 'empty_coin_return',
        'select': 'select_product',
    }

    while True:
        print '{} >'.format(vending_machine.show_display()),
        program_args = raw_input().split()
        if len(program_args) == 0:
            continue
        command = program_args[0].lower()
        options = program_args[1].lower() if len(program_args) > 1 else None
        if command == 'exit':
            break

        elif command == 'menu':
            print '\n', tabulate([
                ['name'] + [x['product_name'] for x in vending_machine.inventory.values()],
                ['cost'] + [x['product_cost'] for x in vending_machine.inventory.values()],
                ['count'] + [x['product_count'] for x in vending_machine.inventory.values()]
            ], ['button'] + vending_machine.inventory.keys(), tablefmt="fancy_grid"), '\n'

        elif command == 'help':
            print """List of Commands:
        > insert [coin_name] -> insert coin of given name, returns True if accepted
        > select [slot_number] -> attempt to purchase product of given slot
        > return -> push coin return button
        > empty -> empty all coins in coin return
        > help -> print this message
        > exit -> exit vending machine program
        """

        else:
            try:
                if options:
                    print getattr(vending_machine, commands[command])(options)
                else:
                    print getattr(vending_machine, commands[command])()
            except KeyError:
                print "Command not recognized; please input another command"


if __name__ == '__main__':
    main()
