# budget-macros

Script for picking the cheapest combination of foods given a set of macronutrient requirements and a database of foods with nutritional and pricing info.

This is sort of a 'multidimensional unbounded knapsack problem' variant, in that items can be repeated indefinitely and there are several requirements to be met - not just one, e.g. weight.

Currently it's brute force, but due to the number of foods being fairly small, the speed is reasonable. Furthermore, the more restrictive the goals the faster it runs, since lots of permutation trees are discarded immediately. Regardless, a Dynamic Programming solution would be better.

# Sample commands and output

Requires python 3.5, argparse

Below are outputs using the foods from food-db to satisfy the macro goals in files bulking-a and cutting-b.

```
> python3.5 budget-calc.py --foods food-db --goals bulking-a
GOALS:
 -> calories: 2700
 -> carbs: 285
 -> fat: 80
 -> protein: 210
==========================================
BRUTE FORCE, ALL MACROS
Performance: 0.8594 s
---------
Cost:     $4.00
Calories: 2732 cal
Protein:  214 g
Carbs:    281 g
Fat:      79 g
Using:
 -> lentils: 4 x 100 g
 -> oatmeal: 2 x 15 g
 -> peanut butter: 6 x 15 g
 -> olive oil: 1 x 15 mL
 -> myprotein impact whey (w/ deal): 5 x 25 g

> python3.5 budget-calc.py --foods food-db --goals cutting-b
GOALS:
 -> calories: 1400
 -> carbs: 35
 -> fat: 60
 -> protein: 180
==========================================
BRUTE FORCE, ALL MACROS
Performance: 0.0191 s
---------
Cost:     $3.73
Calories: 1380 cal
Protein:  177 g
Carbs:    32 g
Fat:      56 g
Using:
 -> oatmeal: 1 x 15 g
 -> peanut butter: 3 x 15 g
 -> olive oil: 1 x 15 mL
 -> myprotein impact whey (w/ deal): 9 x 25 g
```

# Tentative improvements

o implement using Dynamic Programming  
o catch dumb inputs  
o food inputs divided into 1 unit items (15mL w/ 150cal -> 1mL w/ 10cal) to eliminate whole '5 x 15mL' type output  
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
