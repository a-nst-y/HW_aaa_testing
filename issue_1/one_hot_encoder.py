from typing import List, Tuple
import unittest
import pytest


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows

class Testing(unittest.TestCase):
    def test_string(self):
        a = fit_transform(['Moscow', 'New York', 'Moscow', 'London'])
        b = [('Moscow', [0, 0, 1]), ('New York', [0, 1, 0]), \
             ('Moscow', [0, 0, 1]), ('London', [1, 0, 0])]
        self.assertEqual(a, b)
    def test_number(self):
        a = fit_transform([1, 2, 2, 3])
        b = [(1, [0, 0, 1]), (2, [0, 1, 0]), (2, [0, 1, 0]), (3, [1, 0, 0])]
        self.assertEqual(a, b)
    def test_string_not_eq(self):
        a = fit_transform(['Moscow', 'New York', 'Moscow', 'London', 'Moscow', 'Moscow'])
        b = [('Moscow', [0, 0, 1]), ('New York', [0, 1, 0]), ('London', [1, 0, 0])]
        self.assertNotEqual(a, b)
    def test_tuple(self):
        a = fit_transform(('q', 'w', 'e', 'r', 't', 'y'))
        b = [('q', [0, 0, 0, 0, 0, 1]), ('w', [0, 0, 0, 0, 1, 0]), \
             ('e', [0, 0, 0, 1, 0, 0]), ('r', [0, 0, 1, 0, 0, 0]), \
             ('t', [0, 1, 0, 0, 0, 0]), ('y', [1, 0, 0, 0, 0, 0])]
        self.assertEqual(a, b)
    def testraise(self):
        self.assertRaises(TypeError, fit_transform, )

def test_cities():
    cities = ['Moscow', 'New York', 'Moscow', 'London']
    assert fit_transform(cities) == [('Moscow', [0, 0, 1]), \
                                     ('New York', [0, 1, 0]), \
                                     ('Moscow', [0, 0, 1]), \
                                     ('London', [1, 0, 0])]
def test_numbers():
    numbers = [1, 2, 3, 4, 3, 2, 1]
    assert fit_transform(numbers) == [(1, [0, 0, 0, 1]), \
                                      (2, [0, 0, 1, 0]), \
                                      (3, [0, 1, 0, 0]), \
                                      (4, [1, 0, 0, 0]), \
                                      (3, [0, 1, 0, 0]), \
                                      (2, [0, 0, 1, 0]), \
                                      (1, [0, 0, 0, 1])]

def test_tuple():
    number_t = (1, 2, 3, 4, 3, 2, 1)
    assert fit_transform(number_t) == [(1, [0, 0, 0, 1]), \
                                      (2, [0, 0, 1, 0]), \
                                      (3, [0, 1, 0, 0]), \
                                      (4, [1, 0, 0, 0]), \
                                      (3, [0, 1, 0, 0]), \
                                      (2, [0, 0, 1, 0]), \
                                      (1, [0, 0, 0, 1])]
def test_list_of_tuples():
    numbers = [(1, 2), (3, 3), (1, 2)]
    assert fit_transform(numbers) == [((1, 2), [0, 1]), \
                                      ((3, 3), [1, 0]), \
                                      ((1, 2), [0, 1])]
def test_exception():
    with pytest.raises(Exception):
        fit_transform()
    
if __name__ == '__main__':
    from pprint import pprint

    cities = ['Moscow', 'New York', 'Moscow', 'London']
    exp_transformed_cities = [
        ('Moscow', [0, 0, 1]),
        ('New York', [0, 1, 0]),
        ('Moscow', [0, 0, 1]),
        ('London', [1, 0, 0]),
    ]
    transformed_cities = fit_transform(cities)
    pprint(transformed_cities)
    assert transformed_cities == exp_transformed_cities
