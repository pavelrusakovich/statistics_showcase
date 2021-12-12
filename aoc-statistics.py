#!/bin/python3

import random
from typing import List, Dict
from statistics import mean, median
from operator import itemgetter
from sys import maxsize

"""
Suppose, a = [a[0], a[1], ... a[n-1]] , a[i] is a real number 
F(x) = sum( |a[i] - x|   for i in (0..n-1) )
G(x) = sum( (a[i] - x)(a[i] - x - 1)/2  for i in (0..n-1) )

Part 1 - Minimize F(x) for real number x

Notice ,that |x| = x * sgn(x), where 
sgn(x) = 1 if x > 0, 
sgn(x) = 0 if x = 0,
sgn(x) = -1 if x < 0

sgn'(x) = 0 for all x except 0. For x = 0 sgn(x) is not differentiable.

Global minimum of F exists as for extremely large |x|, F(x) -> infinity.
Then Global minimum of F can be found among the points where F'(x) = 0 or doesn't exist.
F'(x) = sum( |a[i] - x|   for i in (0..n-1) )' = 
= sum( (a[i] - x) * sgn(a[i] - x)    for i in (0..n-1) )' = 
= sum( -1 * sgn(a[i] - x) + 0    for i in (0..n-1)) = 
= sum( sgn(x - a[i])   for i in (0..n-1)) for all x where F'(x) is defined.

F'(x) is not defined whenever sgn(a[i] - x) = 0, so not defined for x in a, 
thus, all a[i] are candidates for global minimum. However, we can disqualify any point that is not the local minimum.
Let's re-enumerate a[i] so that they are perfectly ordered and depict them on the X axis.

-----a[0]----a[1]----a[2]---...---a[n-2]----a[n-1]-----
Let's calculate the sign of F'(x) for every interval. This splits into two cases.

Case 1: n is odd. Let's assume n = 2m + 1.
-----a[0]----a[1]----a[2]----...----a[m-1]----a[m]----a[m+1]----...----a[n-2]----a[n-1]-----
 2m+1    2m-1    2m-3    2m-5     3         1      -1         -3   3-2m      1-2m      -2m-1  <- F'(x) for x in interval

From these calculations it's clear that a[m] is the only candidate for which F'(x) changes sign, so it's the only
local minimum of F, therefore, a global minimum. Notably, given the re-enumeration. a[m] is a sample median.

Case 2: n is even. Let's assume n = 2m. 
-----a[0]----a[1]----a[2]----...----a[m-1]----a[m]----a[m+1]----...----a[n-2]----a[n-1]-----
 2m      2m-2    2m-4    2m-6     4         2      0         -2    4-2m      2-2m      -2m    <- F'(x) for x in interval

F'(x) = 0 for entire interval ( a[m], a[m+1] ), so global minimum is in [ a[m], a[m+1] ] as all other candidates are
disqualified.

It appears, that in this case every point on that interval yields the global minimum:
To cut the proof short, I'll put some intuitively clear observations that will take too much time and space to proof
in rigorous way.

If a consists of two elements, b and c (c > b), min(F) is achieved for every b <= x <= c
If a consists on 2m elements, b, b,..b, c, c,..c (b and c repeat m times), then min(F) is achieved for every b <= x <= c
If a consists of 2m elements b-e[0], b-e[1], b-e[m-1], b, c, c+e[m+2], c+e[m+3], .. c+e[2m] (where e[i] > 0), then
since global minimum is achieved for some b <= x <= c, then at least, 
elements less than b need to burn fuel to get to b and, likewise, all elements greater than c need to 
burn fuel at least to get to c, after which the problem is reduced to the previous case.

Note: x = (b + c)/2 is by definition a median of even-sized sample.

######################################
Part 2 - Minimize G(x)

This is even easier, so I'll give less explanation here.
G(x) = sum( (a[i] - x)(a[i] - x - 1)/2  for i in (0..n-1) )
Global minimum exists, G is differentiable for all real x.

G'(x) = sum( -1* (a[i] - x - 1)/2 - (a[i] - x)/2  for i in (0..n-1) ) = 
= sum( x - a[i] + 1/2 for i in (0..n-1) ) = n * x + sum( a[i]for i in (0..n-1) ) + n/2
G'(x) = 0 <=> x = (2 * sum( a[i]for i in (0..n-1) ) - n) / 2n = mean(a) - 1/2.

Note: answer is not exactly a mean due to discretization effect: for H(x) = sum( (a[i] - x)**2 for i in (0..n-1)), 
minimum will be achieved exactly at mean.

Note: after the problem is solved in continuous form, translating it into discrete form is very easy,
but must not be overlooked.
"""


class RandomList:
    length: int
    upper_bound: int
    lower_bound: int
    _items: List[int]
    _compressed_items: Dict

    def mean(self):
        return round(mean(self._items) - 1 / 2)

    def median(self):
        return median(self._items)

    def __init__(self, items_c, lo, hi):
        self._items = []
        self._compressed_items = {}
        self.lower_bound = lo
        self.upper_bound = hi
        for i in range(items_c):
            item = random.randint(lo, hi)
            self._items.append(item)
            if item in self._compressed_items:
                self._compressed_items[item] += 1
            else:
                self._compressed_items[item] = 1

    def linear_fuel_burn(self, target):
        return sum(abs(pos - target) * count for pos, count in self._compressed_items.items())

    def minimum_burn(self, func):
        min_burn, pos_min_burn = min(
            [(func(j), j) for j in range(self.lower_bound, self.upper_bound)]
            , key=itemgetter(0))
        return min_burn

    def arithmetic_progression_burn(self, target):
        return sum(
            abs((pos - target) * (pos - target - 1) / 2) * count for pos, count in self._compressed_items.items())

    def __str__(self):
        return self._items.__str__()


if __name__ == "__main__":
    seed = random.randrange(maxsize)
    print(f'Random seed: {seed}')
    random.seed(seed)
    for i in range(10):
        size = random.randint(1, 100)
        sample = RandomList(size, 0, random.randint(10, 1000))
        passed = True
        print(f' \nTEST {i + 1} \n List of {size} items: \n {sample}')
        try:
            assert (sample.minimum_burn(sample.linear_fuel_burn) == sample.linear_fuel_burn(sample.median()))
        except AssertionError as e:
            print(f'FAILED: Median was not the optimal alignment point for linear fuel consumption \n '
                  f'Median yields {sample.linear_fuel_burn(sample.median())}, '
                  f'optimum is {sample.minimum_burn(sample.linear_fuel_burn)}')
            passed = False
        try:
            assert (sample.minimum_burn(sample.arithmetic_progression_burn) ==
                    sample.arithmetic_progression_burn(sample.mean()))
        except AssertionError as e:
            print(f'FAILED: "Mean" was not the optimal alignment point for arithmetic-progressive fuel consumption \n '
                  f'"Mean" yields {sample.arithmetic_progression_burn(sample.mean())}, '
                  f'optimum is {sample.minimum_burn(sample.arithmetic_progression_burn)} ')
            passed = False

        if passed:
            print("PASSED")


