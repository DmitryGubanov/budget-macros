# budget-macros

Script for picking the cheapest combination of foods given a set of macronutrient requirements and a database of foods with nutritional and pricing info.

This is sort of a 'multidimensional unbounded knapsack problem' variant, in that items can be repeated indefinitely and there are several requirements to be met - not just one. This type of problem is NP-hard.

budget-calc.py contains code for a lot of different implementations for the solution, but there are three implementations of note: top-down brute force, top-down dynamic programming, and bottom-up dynamic programming. For a relatively normal diet (<2500 calories) and a small set of foods (<8 foods), a top down brute force solution performs best. However, once you increase the requirements or the set of foods, the dynamic programming solutions start to outperform the brute force solution. I go into more detail in the performance section.

# Sample commands and output

Requires python 3.5, argparse

Below are outputs using the foods from food-db to satisfy the macro goals in files bulking-a and cutting-b.

```
$ python budget-calc.py --foods food-db --goals bulking-a
GOALS:
 -> calories: 2700
 -> carbs: 285
 -> fat: 80
 -> protein: 210
==========================================
BRUTE FORCE, ALL MACROS
Performance: 8.6511 s
---------
Cost:     $3.99
Calories: 2732 cal
Protein:  213 g
Carbs:    288 g
Fat:      76 g
Using:
 -> oatmeal: 1 x 45 g
 -> peanut butter: 5 x 15 g
 -> olive oil: 4 x 5 mL
 -> myprotein impact whey (w/ deal): 5 x 25 g
 -> lentils: 4 x 100 g
==========================================
DYNAMIC PROGRAMMING (TOP-DOWN), ALL MACROS
Performance: 7.2987 s
---------
Cost:     $3.93
Calories: 2672 cal
Protein:  210 g
Carbs:    285 g
Fat:      73 g
Using:
 -> lentils: 4 x 100 g
 -> oatmeal: 1 x 45 g
 -> peanut butter: 4 x 15 g
 -> olive oil: 5 x 5 mL
 -> myprotein impact whey (w/ deal): 5 x 25 g
```
```
 $ python budget-calc.py --foods food-db --goals cutting-b
 GOALS:
  -> calories: 1400
  -> carbs: 35
  -> fat: 60
  -> protein: 180
 ==========================================
 BRUTE FORCE, ALL MACROS
 Performance: 0.0360 s
 ---------
 Cost:     $4.10
 Calories: 1410 cal
 Protein:  184 g
 Carbs:    36 g
 Fat:      56 g
 Using:
  -> whole milk: 1 x 1 cup
  -> peanut butter: 3 x 15 g
  -> olive oil: 1 x 5 mL
  -> myprotein impact whey (w/ deal): 9 x 25 g
 ==========================================
 DYNAMIC PROGRAMMING (TOP-DOWN), ALL MACROS
 Performance: 0.1142 s
 ---------
 Cost:     $4.13
 Calories: 1370 cal
 Protein:  178 g
 Carbs:    30 g
 Fat:      58 g
 Using:
  -> whole milk: 1 x 1 cup
  -> peanut butter: 1 x 15 g
  -> olive oil: 5 x 5 mL
  -> myprotein impact whey (w/ deal): 9 x 25 g
```

# Performance

This section is to detail what I found with regards to the performance of various algorithms used. I'll be using this section to solidify the ideas I had in my mind, as a guide from which to build further optimizations, and as a reference for the future.

### Estimating run-times

Here are all the estimated run times in one area; they'll be used for reference purposes in the next sections too.

##### Top-down brute force
O(2<sup>N</sup>), where N is linearly correlated to:
- the ratio between the goal nutrient sizes and the food nutrient sizes, i.e. cutting food servings in half would impact performance similarly to doubling your goals (e.g. 2000 cal -> 4000 cal)
- the number of foods in the food database

##### Top-down dynamic programming
O(2<sup>M</sup>), where M is similar to N.

##### Bottom-up dynamic programming
O(Ccfpn), where:
- C is the caloric goal
- c is the carbs goal
- f is the fat goal
- p is the protein goal
- n is the number of foods in the database

### Top-down brute force

For a typical diet (<2500 calories and a more-or-less balanced set of macronutrient requirements) with <8 different foods/meals in the database, this is the best option. However, increasing the requirements by a factor of two or even doubling the number of foods in the database makes the runtime for this solution explode.

### Top-down dynamic programming

Technically, the runtime is the 'same' as brute force here. There is added run time for maintaining a data structure, but lost run time due to overlaps. The overlaps are hightly dependent on the foods in the database.

As an experiment, I tried two alterations to the database: tripled the foods by literally copy and pasting the database two more times, and doubling the amount of foods by adding a new set of foods. In the former case, the dynamic programming approach was much faster than brute force, since there were a lot of overlaps (the foods combinations would be calculated three times). However, in the latter, the run times both grew together, since there were no or few overlaps.

### Bottom-up dynamic programming

Although this is the 'best' in terms of scalability, the run time starts at an incredibly high number. With a typical diet and <8 foods in the databse, brute force takes <500,000 steps; whereas this algorithm takes around 100 billion. Granted, adding more foods and increasing the requirements would quickly make this outperform top-down, that simply means top-down is not usable after some point while this is never usable.

### Conclusions and future improvements/testing

All algorithms are slow, but top-down is at least usable at some points. A bottom up approach shines when you ignore at least 2 requirements (say you only care about calories and protein), but fails with any more.

I can use this analysis to develop a system which estimates the most reasonable algorithm to use given a set of inputs, at the cost of some time performing calculations on the input. Furthermore, it'll probably be wise to implement a non-deterministic solution or some greedy algorithm which approximates a solution.

I think the way food nutrition numbers are naturally distributed allows for some shortcuts to be taken that would otherwise not work with a completely random set of numbers.

# Tentative improvements

x implement using Dynamic Programming bottom-up  
x implement using Dynamic Programming top-down  
o implement a greedy algorithm  
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

> Goals: efficiency

- top-down and bottom-up dynamic programming implementations
