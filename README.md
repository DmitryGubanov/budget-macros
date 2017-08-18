# budget-macros

Script for picking the cheapest combination of foods given a set of macronutrient requirements and a database of foods with nutritional and pricing info.

This is sort of a 'multidimensional unbounded knapsack problem' variant, in that items can be repeated indefinitely and there are several requirements to be met - not just one, e.g. weight.

Currently it's brute force, but due to the number of foods being fairly small, the speed is reasonable. Furthermore, the more restrictive the goals the faster it runs, since lots of permutation trees are discarded immediately. Regardless, a Dynamic Programming solution would be better.

# Sample commands

Requires python 3.5, argparse

```
python3.5 budget-calc.py --foods food-db --goals bulking-a
python3.5 budget-calc.py --foods food-db --goals cutting-b
```

This will output the foods used from the food-db to satisfy the macro goals in files bulking-a and cutting-b.


# Tentative improvements

o implement using Dynamic Programming  
o catch dumn inputs  
o optional requirements (e.g. don't care about carbs)  
o flexible requirements (e.g. protein AT LEAST X g, carbs AT MOST X g)  
o meals (options are combos of food, rather than indv food items)  
o not necessarily starting at 0 foods eaten (e.g. you want to eat a cake, so given you ate cake, now what)

# Version features/changelog

Current version: 0.1  
WIP: 0.2

## Version 0.1

> Goals: just get the correct answer

- implement a brute force solution for a goal containing all macros
- works for all correct/possible inputs (doesn't handle if goals are literally impossible)

## Version 0.2

> Goals: efficiency, correctness
