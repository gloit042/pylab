import curry as c
from copy import deepcopy

class TryModError(Exception):
    pass
class TakeError(Exception):
    pass

class FIterable(object):
    def __init__(self, init_val, iterate_func):
        self.first = True
        self.r = init_val
        self.next_func = iterate_func
    def __iter__(self):
        return self
    def __next__(self):
        if self.first:
            self.first = False
            return self.r
        
        self.r = self.next_func(self.r)
        return self.r

class LazyList(object):
    def __init__(self, init_val, 
            iterate_func = lambda x: x + 1,
            filter_func = lambda x: True,
            drop_while = lambda x: False):
        self.__len__ = 0
        self.__evaled__ = []
        self.__not_evaled__ = FIterable(init_val, iterate_func)
        self.filter_func = filter_func
        self.drop_while = drop_while
        self.stop = False

    def __repr__(self):
        if self.stop:
            return repr(self.__evaled__)
        else:
            return repr(self.__evaled__) + ' + [unevaluated]'

    def __str__(self):
        if self.stop:
            return str(self.__evaled__)
        else:
            return str(self.__evaled__) + ' + [unevaluated]'

    def __iter__(self):
        if self.stop:
            return iter(self.__evaled__)
        self.index = 0
        return self

    def __next__(self):
        self.index = self.index + 1
        return self[self.index - 1]

    def __getitem__(self, key):
        if isinstance(key, slice):
            if self.stop:
                return self.__evaled__[key]
            raise IndexError("Lazy list doesn't support slice indexing")

        if key < 0:
            if self.stop:
                return self.__evaled__[key]
            raise IndexError("Minus key not allowed when list isn't entirely evauated!");
        if key < self.__len__:
            return self.__evaled__[key]

        while self.__len__ <= key:
            t = self.__not_evaled__.__next__()
            if self.filter_func(t):
                if self.drop_while(t):
                    self.stop = True;
                    raise IndexError("Out of range")
                self.__len__ = self.__len__ + 1
                self.__evaled__.append(t)

        return self.__evaled__[key]

    def __setitem__(self, key, val):
        raise TryModError("Lazy list can't be modified!")

    def eval_all(self):
        t = self.iterate_func(self.__evaled__[-1])
        while not self.stop:
            if self.filter_func(t):
                if self.drop_while(t):
                    self.stop = True;
                    break
                self.__len__ = self.__len__ + 1
                self.__evaled__.append(t)
            t = self.iterate_func(t)




def repeat(N):
    return LazyList(N, iterate_func = c.__id__)

def iterate(N, f = None):
    if f == None:
        return repeat(N)
    else:
        return LazyList(N, iterate_func = f)

def __take__(n, L):
    if n <= 0:
        raise TakeError("can't take non-positive number elements")
    i = 0
    r = []
    for v in L: 
        r.append(v)
        i = i + 1
        if i == n:
            return r

__lib_filter__ = filter
def __filter__(f, L):
    T = deepcopy(L)
    T.__evaled__ = list(__lib_filter__(f, L.__evaled__))
    T.filter_func = lambda x: f(x) and L.filter_func(x)
    return T

def __take_while__(f, L):
    s = iter(L)
    r = []
    t = s.__next__()
    while f(t):
        r.append(t)
        t = s.__next__()
    return r

filter = c.C(__filter__)
take = c.C(__take__)
takeWhile = c.C(__take_while__)
