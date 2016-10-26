# The Vending Machine Kata

## Requirements

The following are needed in advance to run the Vending Machine:

* Python 2.7+
* Pip

To maintain work environment purity, a virtual environment is recommended. I recommended taking a look at [this](http://virtualenvwrapper.readthedocs.io/en/latest/) for more information.

## Setup

#### Project Organization
```
| ./vending-machine-kata (root directory)
|   |-- test
|   |   |-- __init__.py
|   |   `-- test_vending_machine.py
|   |
|   |-- vending_machine
|   |   |-- __init__.py
|   |   |-- coins.json
|   |   |-- products.json
|   |   |-- run_vending_machine.py
|   |   `-- vending_machine.py   
|   |
|   |-- README.md
|   |-- requirements.txt
|   `-- .gitignore
```

#### Installation
To install the required python modules, navigate to the project root directory `./vending-machine-kata` and run:
```
./pip install -r requirements.txt
```

## Running Tests

To run tests, navigate to the project root directory `./vending-machine-kata` and run:
```
./py.test
```

## Running The Vending Machine

To run the interactive vending machine CLI program, navigate to the project root directory `./vending-machine-kata` and run:

```
./python vending_machine/run_vending_machine.py [-h] [coins_file] [products_file]
```

#### Help Message

To see help message about running `run_vending_machine.py` type:
```
> ./python run_vending_machine.py -h
```

message:
```
usage: run_vending_machine.py [-h] [coins_file] [products_file]

A CLI Vending Machine. After running type help for more commands

positional arguments:
  coins_file     Location for the JSON file of initial coin definitions
  products_file  Location for the JSON file of initial product definitions

optional arguments:
  -h, --help     show this help message and exit
```
after running type `help` for more information:

```
INSERT COIN > help
List of Commands:
        > insert [coin_name] -> insert coin of given name, returns True if accepted
        > select [slot_number] -> attempt to purchase product of given slot
        > return -> push coin return button
        > empty -> empty all coins in coin return
        > help -> print this message
        > exit -> exit vending machine program
```


## Input Files

#### Coins.json

A JSON formatted input file that run_vending_machine.py utilizes to initalize coin state.

e.g.
```
[
    {"coin_name": "nickel", "coin_value": 5, "coin_count": 10},
    {"coin_name": "dime", "coin_value": 10, "coin_count": 10},
    {"coin_name": "quarter", "coin_value": 25, "coin_count": 10}
]
```

#### Products.json

A JSON formatted input file that run_vending_machine.py utilizes to initalize product state.

e.g.
```
[
    {"product_name": "cola", "product_cost": 100},
    {"product_name": "chips", "product_cost": 50, "product_count": 10},
    {"product_name": "candy", "product_cost": 65, "product_count": 10}
]
```
## Assumptions

This is a list of assumptions that were made about the functioning of this vending machine:

* No two coins have the same value or name
* The ability to store coins and products is arbitrarily large
* Inserted coins are added to the register after a successful purchase
* All larger coins can be made with a combination of smaller coins
* EXACT CHANGE ONLY is displayed when the register is completely empty, and instead...
* A NEW DISPLAY MESSAGE WAS ADDED, "UNABLE TO MAKE CHANGE", which displays when:
 * Inserted value exceeds vending machine's ability to make change for a selected product
