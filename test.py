import lazy as l
import time

s = l.repeat(1)

def unit_test(test_name):
    def time_scale(func):
        def wrapper(*args, **kwargs):
            print('Test case: ' + test_name)
            print('Output:')
            starttime = time.time()
            func(*args, **kwargs)
            endtime = time.time()
            print('elapsed: %d ms' % ((endtime - starttime) * 1000))
            print('')
        return wrapper
    return time_scale

@unit_test('take')
def take_test(n):
    print(sum(l.take (n) (s)))

@unit_test('takeWhile')
def takeWhile_test(n):
    print(sum(l.takeWhile (lambda x: x < n) (l.LazyList())))

if __name__ == '__main__':
    take_test(10000000)
    takeWhile_test(10000000)


