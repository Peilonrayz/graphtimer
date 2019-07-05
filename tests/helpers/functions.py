import time
import math

from graphtimer import TimerNamespace


class UnoptimisedRange(object):
    def __init__(self, size):
        self.size = size

    def __getitem__(self, i):
        if i >= self.size:
            raise IndexError()
        return i


class Peilonrayz(TimerNamespace):
    def test_comprehension(iterable):
        return [i for i in iterable]

    def test_append(iterable):
        a = []
        append = a.append
        for i in iterable:
            append(i)
        return a


SCALE = 10.


class Graipher(TimerNamespace):
    def test_o_n(n):
        time.sleep(n / SCALE)

    def test_o_n2(n):
        time.sleep(n ** 2 / SCALE)

    def test_o_log(n):
        time.sleep(math.log(n + 1) / SCALE)

    def test_o_exp(n):
        time.sleep((math.exp(n) - 1) / SCALE)

    def test_o_nlog(n):
        time.sleep(n * math.log(n + 1) / SCALE)


class Reverse(TimerNamespace):
    def test_orig(stri):
        output = ''
        length = len(stri)
        while length > 0:
            output += stri[-1]
            stri, length = (stri[0:length - 1], length - 1)
        return output

    def test_g(s):
        return s[::-1]

    def test_s(s):
        return ''.join(reversed(s))


SCALES_SCALE = 1000


class Scales(TimerNamespace):
    def test_o_log(n):
        time.sleep(math.log(n + 1) / (n ** n / 1) / SCALES_SCALE)

    def test_o_n(n):
        time.sleep(n / (n ** n / 1) / SCALES_SCALE)

    def test_o_nlog(n):
        time.sleep(n * math.log(n + 1) / (n ** n / 1) / SCALES_SCALE)

    def test_o_n2(n):
        time.sleep(n ** 2 / (n ** n / 1) / SCALES_SCALE)

    def test_o_n3(n):
        time.sleep(n ** 3 / (n ** n / 1) / SCALES_SCALE)

    def test_o_2_n(n):
        time.sleep((2 ** n - 1) / (n ** n / 1) / SCALES_SCALE)

    def test_o_e_n(n):
        time.sleep((math.exp(n) - 1) / (n ** n / 1) / SCALES_SCALE)

    def test_o_n_n(n):
        time.sleep((n ** n - 1) / (n ** n / 1) / SCALES_SCALE)
