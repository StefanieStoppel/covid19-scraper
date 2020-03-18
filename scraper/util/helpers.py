from itertools import zip_longest

"""Collect data into fixed-length chunks or blocks"""
def grouper(iterable, n, fillvalue=None):
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return list(zip_longest(fillvalue=fillvalue, *args))