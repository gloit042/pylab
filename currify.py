import functools as f
from inspect import signature
import sys
from copy import deepcopy

'function composition'

class compose(object):
    def __init__(self, func, chain = []):
        if func == None:
            if chain == []:
                print('Error: empty input')
            else:
                self.chain = deepcopy(chain)
            return
        if callable(func):
            n = len(signature(func).parameters)
            if len != 0:
                self.chain = deepcopy(chain)
                self.chain.append(func)
            else:
                print('Error: not callable')
        else:
            print('Error: not callable')

    def __call__(self, feed):
        func = self.chain[-1]
        nfunc = f.partial(func, feed)
        n = len(signature(nfunc).parameters)
        if n == 0:
            if len(self.chain) == 1:
                return nfunc()
            else:
                return compose(None, self.chain[0:-1])(nfunc())
        else:
            if len(self.chain) == 1:
                return compose(None, [nfunc])
            else:
                return compose(None, self.chain[0:-1] + [nfunc])

    def __pow__(self, other):
        return compose(__id__, self.chain + other.chain)


def __id__(x):
    return x

add = compose(lambda x, y: x + y)
minus = compose(lambda y, x: x - y)
multiply = compose(lambda x, y: x * y)
divide = compose(lambda y, x: x / y)
