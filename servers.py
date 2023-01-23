#!/usr/bin/python
# -*- coding: utf-8 -*-

# !/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional
from abc import ABC, abstractmethod
from typing import TypeVar, List, Optional, Dict
import numbers

import re


class Product:
    def __init__(self, name: str, price: float):

        if isinstance(name, str) and isinstance(price, numbers.Number):
            if re.fullmatch(r'[a-zA-Z]+[0-9]+', name) is not None:
                self.name: str = name
                self.price: float = price
            else:
                raise ValueError
        else:
            raise ValueError

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


class Server(ABC):

    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs):
        self.products = []

    @abstractmethod
    def get_entries(self, n_letters: int = 2) -> List[Product]:
        raise NotImplemented


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products: List[Product] = products

    def get_entries(self, n_letters: int = 2) -> List[Product]:
        results: List[Product] = []
        for product in self.products:
            num_of_letter = 0
            num_of_digits = 0
            for sign in product.name:
                if sign.isalpha():
                    num_of_letter += 1
                if sign.isdigit():
                    num_of_digits += 1
            if num_of_letter == n_letters:
                if num_of_digits == 2 or num_of_digits == 3:
                    results.append(product)
        if len(results) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted(results, key = lambda prod: prod.price)


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products = {product.name: product for product in products}

    def get_entries(self, n_letters: int = 2) -> List[Product]:
        results: List[Product] = []
        for product in self.products.values():
            num_of_letter = 0
            num_of_digits = 0
            for sign in product.name:
                if sign.isalpha():
                    num_of_letter += 1
                if sign.isdigit():
                    num_of_digits += 1
            if num_of_letter == n_letters:
                if num_of_digits == 2 or num_of_digits == 3:
                    results.append(product)
        if len(results) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError
        else:
            return sorted(results, key = lambda prod: prod.price)


class Client:
    def __init__(self, server: Server) -> None:
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            total_price: float = 0
            for product in self.server.get_entries(n_letters):
                total_price += product.price
            if total_price == 0:
                return None
            return total_price
        except TooManyProductsFoundError:
            return None
