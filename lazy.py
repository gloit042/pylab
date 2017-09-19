import curry as c

class TryModError(Exception):
    pass

class LazyList(object):
    def __init__(self, init_val, 
            iterate_func = lambda x: x + 1,
            filter_func = lambda x: True,
            drop_while = lambda x: False):
        if filter_func(init_val):
            self.__len__ = 1
            self.__evaled__ = [init_val]
        else:
            self.__len__ = 0
            self.__evaled__ = []
        self.iterate_func = iterate_func
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

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise IndexError("Lazy list doesn't support slice indexing")

        if key < 0:
            if self.stop:
                return self.__evaled__[key]
            raise IndexError("Minus key not allowed when list isn't entirely evauated!");
        if key < self.__len__:
            return self.__evaled__[key]

        t = self.iterate_func(self.__evaled__[-1])
        while self.__len__ <= key:
            if self.filter_func(t):
                if self.drop_while(t):
                    self.stop = True;
                    raise IndexError("Out of range")
                self.__len__ = self.__len__ + 1
                self.__evaled__.append(t)
            t = self.iterate_func(t)

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
