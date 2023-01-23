import unittest
from collections import Counter

import servers
from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)

class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

# czy wyniki zwracane przez get_entries są poprawnie posgregowane:
    def test_get_entries_is_sorted(self):
        products = [Product('Pd12', 2), Product('PP234', 3), Product('PP225', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[0], products[1]]), Counter(entries))

# Czy przekroczenie maksymalnej liczby znalezionych produktów powoduje rzucenie wyjątku?
    def test_get_entries_error(self):
        products = [Product('Pd12', 2), Product('Hx45',2), Product('PP234', 3), Product('PP225', 1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

# Czy funkcja obliczająca łączną cenę produktów zwraca poprawny wynik w przypadku rzucenia wyjątku oraz braku produktów pasujących do kryterium wyszukiwania?
    def test_total_price_if_too_many(self):
        products = [Product('Pd12', 2), Product('Hx45',2), Product('PP234', 3), Product('PP225', 1)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_if_too(self):
        products = [Product('Pd12', 2), Product('Hx45',2), Product('PP234', 3), Product('PP225', 1)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(1))


if __name__ == '__main__':
    unittest.main()