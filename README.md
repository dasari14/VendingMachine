# The Vending Machine Kata

## Requirements

The following are needed in advance to run the Vending Machine:

* Python 2.7+
* Pip

To maintain work environment purity, a virtual environment is recommended. I recommended taking a look at [this](http://virtualenvwrapper.readthedocs.io/en/latest/) for more information.

## Setup

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

To run the vending machine program, navigate to the project root directory `./vending-machine-kata` and run:

```
./python vending_machine/vending_machine.py
```

## Assumptions

This is a list of assumptions that were made about the functioning of this vending machine:

* No two coins have the same value or name
* The ability to store coins and products is arbitrarily large
* Inserted coins are added to the register after a successful purchase
* EXACT CHANGE ONLY is displayed when the register is completely empty, and instead...
* ###### A NEW DISPLAY MESSAGE WAS ADDED, "UNABLE TO MAKE CHANGE", which displays when:
 * Inserted value exceeds vending machine's ability to make change for a selected product
 * Inserted value exceeds $1.00 and vending machine is unable to make change for any product
