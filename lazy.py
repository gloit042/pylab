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
        self.init = init_val
        self.__next_func__ = iterate_func
    def __iter__(self):
        return self
    def __next__(self):
        if self.first:
            self.first = False
            return self.r
        
        self.r = self.__next_func__(self.r)
        return self.r
    def new(self):
        return FIterable(self.init, self.__next_func__)

class LazyList(object):
    def __init__(self,
            init_val = 0, 
            iterate_func = lambda x: x + 1,
            filter_func = lambda x: True,
            drop_while = lambda x: False):
        self.__len__ = 0
        self.__evaled__ = []
        self.__not_evaled__ = FIterable(init_val, iterate_func)
        self.__filter_func__ = filter_func
        self.__drop_while__ = drop_while
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
            if self.__filter_func__(t):
                if self.__drop_while__(t):
                    self.stop = True;
                    raise IndexError("Out of range")
                self.__len__ = self.__len__ + 1
                self.__evaled__.append(t)

        return self.__evaled__[key]

    def __setitem__(self, key, val):
        raise TryModError("Lazy list can't be modified!")

    def eval_all(self):
        if not self.stop:
            for i in self.__not_evaled__:
                if self.__drop_while__(i):
                    self.stop = True
                    break
                if self.__filter_func__(i):
                    self.__evaled__.append(i)




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
    _ = L[n - 1]
    r = L.__evaled__[0:n]
    return r

__lib_filter__ = filter
def __filter__(f, L):
    T = LazyList()
    T.filter_func = lambda x: f(x) and L.filter_func(x)
    T.drop_while = L.drop_while
    T.__not_evaled__ = L.__not_evaled__.new()
    return T

def __take_while__(f, L):
    S = deepcopy(L)
    S.__drop_while__ = lambda x: not f(x) or L.__drop_while__(x)
    t = list(map(S.__drop_while__, S.__evaled__))
    if True in t:
        return S.__evaled__[:t.index(True) + 1]
    else:
        S.eval_all()
        return S.__evaled__[:]

filter = c.C(__filter__)
take = c.C(__take__)
takeWhile = c.C(__take_while__)
