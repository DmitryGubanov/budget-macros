# budget-macros

Script for picking the cheapest combination of foods given a set of macronutrient requirements and a database of foods with nutritional and pricing info.

This is sort of a 'multidimensional unbounded knapsack problem' variant, in that items can be repeated indefinitely and there are several requirements to be met - not just one.

budget-calc.py contains code for a lot of different implementations for the solution, but there are three implementations of note: top-down brute force, top-down dynamic programming, and bottom-up dynamic programming. I was surprised to find that, with reasonable inputs, brute force actually outperforms the dynamic programming solutions. That's not necessarily a bad thing, considering a human diet doesn't consist of many foods (for a computer), so all the combinations that satisfy the requirements isn't really that many combinations. I go into more detail in the next section.

# Notes on performance

After some testing, I've concluded that a top-down brute force algorithm is actually best for performance for calculating a diet satisfying all requirements. If the numbers were truly random, this might not be the case; but I believe - due to the distribution in the numbers representing food nutrition - brute force does not actually end up calculating overlapping problems, rendering a dynamic programming solution pointless.

I've tried a top-down dynamic programming solution, but as I mentioned, brute force doesn't solve overlapping problems in this case. As a result, the data structures maintained for dynamic programming add run time on top of the brute force run time.

I've also tried a bottom-up dynamic programming solution. However, this consistently runs in O(Ccfpn) time. Where C is the calorie goal, c is the carbs goal, f is fat goal, p is protein goal, and n is number of foods in the database. The average diet requirements with 10 different foods puts this number at around 100 billion. Most tests I've ran in brute force only took ~300,000 steps at most.

Furthermore, with stricter diets (low carb or low fat, for example), a lot of paths of the permutation tree created by brute force recursion end up being cut short due to a lot of foods violating those strict restrictions. This gives an even bigger edge to brute force in these cases.

If the food database was more granular (instead of foods being something like 200 cal/30 carbs/10 protein/4 fat they were more like 2 cal/0.3 carbs/0.1 protein/0.04 fat) the integer solutions would have overlaps and dynamic programming would be more effective relative to brute force. However, rounding errors would be introduced with integer solutions. With floats, the data structure needed to maintain all solutions would be ridiculously complex and would again be the bottleneck.

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

x implement using Dynamic Programming bottom-up  
o write mapping function, given requirements, perform predicted fastest solution method  
o catch dumb inputs  
o ~~food inputs divided into 1 unit items (15mL w/ 150cal -> 1mL w/ 10cal) to eliminate whole '5 x 15mL' type output~~ multiply an output like '5 x 15mL' so it says '75ml' in brackets beside it  
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

- top-down and bottom-up dynamic programming implementations
