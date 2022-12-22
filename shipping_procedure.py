"""Shipping procedures for Ubermelon."""

import sys
from melons import Melon, Squash
import robots

MELON_LIMIT = 200


def show_help():
    """Displays info about this program."""

    print("""
    shipping_procedure.py
      Master Control Program for Automated Melon Order Fulfillment

    This program processes orders from an order log file and controls the
    robots used to fulfill the orders.

    Usage:

        python shipping_procedure.py [logfile]

    Where:

        [logfile]
            The name of the log file you would like to process.
            Hint: There are two files included in this project folder.
    """)


def assess_and_pack_orders():
    """Assesses and packs order objects.

    Distinguishes between melons/squashes."""

    # Check to make sure we've been passed an argument on the
    # command line.  If not, display instructions.
    if len(sys.argv) < 2:
        show_help()
        return

    # Get the name of the log file to open from the command line
    logfilename = sys.argv[1]

    # Open the log file
    file = open(logfilename)

    # Read each line from the log file and process it

    for line in file:

        # Each line should be in the format:
        # <melon name>: <quantity>
        melon_type, quantity = line.rstrip().split(':')
        quantity = int(quantity)

        print("\n-----")
        print(f"Fulfilling order of {quantity} {melon_type}")
        print("-----\n")

        count = 0
        melons = []

        # Pick melons until we reach the requested quantity

        while len(melons) < quantity:

            # Make sure we haven't reached our limit for the total
            # number of melons we're allowed to pick
            if count > MELON_LIMIT:
                print("\n------------------------------")
                print("ALL MELONS HAVE BEEN PICKED")
                print("ORDERS FAILED TO BE FULFILLED!")
                print("------------------------------\n")
                return

            # Have the robot pick a 'melon' -- check to
            # see if it is a Winter Squash or not.
            if melon_type != "Winter Squash":
                melon = Melon(melon_type)

            else:
                melon = Squash(melon_type)

            robots.pickerbot.pick(melon)
            count += 1

            # Prepare the melon
            melon.prep()

            # Evaluate the melon
            presentable = robots.inspectorbot.evaluate(melon)

            if presentable:
                melons.append(melon)

            else:
                robots.trashbot.trash(melon)
                continue

        print("------")
        print(f"Robots Picked {count} {melon_type} for order of {quantity}")

        # Pack the melons for shipping
        boxes = robots.packerbot.pack(melons)

        # Ship the boxes
        robots.shipperbot.ship(boxes)

        print("------\n")

assess_and_pack_orders()
