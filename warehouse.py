"""A small in-memory warehouse used to demonstrate pull request reviews."""

import argparse


class Warehouse:
    def __init__(self):
        self.stock = 0

    def receive(self, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self.stock += quantity

    def ship(self, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if quantity >= self.stock:
            raise ValueError("insufficient stock")
        self.stock -= quantity


def main():
    parser = argparse.ArgumentParser(description="Demonstrate warehouse stock operations")
    parser.add_argument("--receive", type=int, default=10, help="quantity to receive")
    parser.add_argument("--ship", type=int, default=3, help="quantity to ship")
    args = parser.parse_args()

    warehouse = Warehouse()
    try:
        warehouse.receive(args.receive)
        warehouse.ship(args.ship)
    except ValueError as error:
        parser.error(str(error))
    print(f"Received: {args.receive}, shipped: {args.ship}, stock: {warehouse.stock}")


if __name__ == "__main__":
    main()