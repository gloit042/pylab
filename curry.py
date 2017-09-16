import functools as f
from inspect import signature
import sys
from copy import deepcopy

'A curry util'
'only availble for constant arguments function'

class C(object):

    'Curry function object'

    def __init__(self, func, chain = []):
        if func == None:
            if chain == []:
                print('Error: empty input')
            else:
                self.chain = deepcopy(chain)
            return
        if callable(func):
            try:
                n = len(signature(func).parameters)
            except ValueError as e:
                print('Varied arguments function cannot be currified: ', func)
                return None
            if len != 0:
                self.chain = deepcopy(chain)
                self.chain.append(func)
            else:
                print('Error: not callable')
        else:
            print('Error: not callable')

    def __call__(self, *feed):
        func = self.chain[-1]
        nfunc = f.partial(func, feed[0])
        n = len(signature(nfunc).parameters)
        if len(feed) > 1:
            if n == 0:
                if len(self.chain) == 1:
                    return nfunc()(feed[1])
                else:
                    feed[0] = nfunc()
                    return C(None, self,chain[0:-1])(*feed)
            else:
                if len(self.chain) == 1:
                    return C(None, [nfunc])(*feed[1:])
                else:
                    return C(None, self.chain[0:-1] + [nfunc])(*feed[1:])
        if n == 0:
            if len(self.chain) == 1:
                return nfunc()
            else:
                return C(None, self.chain[0:-1])(nfunc())
        else:
            if len(self.chain) == 1:
                return C(None, [nfunc])
            else:
                return C(None, self.chain[0:-1] + [nfunc])

    def __pow__(self, other):
        if not callable(other):
            raise TypeError('Not callable: %s' % other)
        return C(__id__, self.chain + other.chain)


def __id__(x):
    return x

def __foldl__(f, init, l):
    if len(l) > 1:
        return __foldl__(f, f(init, l[0]), l[1:])
    else:
        return f(init, l[0])

def __concat_two__(l, r):
    if type(l) is not type([]):
        print('Not a list: %s' % l)
        return None
    if type(r) is not type([]):
        print('Not a list: %s' % r)
        return None
    return l + r


add = C(lambda x, y: x + y)
minus = C(lambda y, x: x - y)
multiply = C(lambda x, y: x * y)
divide = C(lambda y, x: x / y)

M = map
map = C(lambda x, y: list(M(x,y)))

foldl = C(__foldl__)

take = C(lambda x, y: y[0:x])
concat = C(lambda x:foldl (C(__concat_two__)) ([]) (x))

