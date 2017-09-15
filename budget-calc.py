#!/usr/bin/python

import argparse
import time

dp = {}

def build_foods(filename):
    """Reads a file, builds the foods with their characteristics, and
    returns them in a list.

    Args:
        filename: A file name for the file containing the food data

    Returns:
        A list of dictionaries?
    """
    foods = []
    with open(filename, 'r') as file:
        for line in file:
            food = {}
            (name, cost, amount, serving, unit, calories,
             carbs, fat, protein) = line.strip().split(',')
            food['name'] = name
            food['serving_cost'] = float(cost) * float(serving) / float(amount)
            food['serving_size'] = serving + ' ' + unit
            food['calories'] = float(calories)
            food['carbs'] = float(carbs)
            food['fat'] = float(fat)
            food['protein'] = float(protein)
            foods.append(food)
    return foods


def build_goals(filename):
    """Reads a file, builds the goals, and returns them in a
    dictionary.

    Args:
        filename: A file name for the file containing the goal data

    Returns:
        A dictionary? containing goals mapped to values.
    """
    goals = {}
    macros = ['calories', 'carbs', 'fat', 'protein']
    with open(filename, 'r') as file:
        for line in file:
            reqs = line.strip().split(',')
            for i, macro in enumerate(macros):
                if reqs[i] == '-1':
                    continue
                goals[macros[i]] = float(reqs[i][1:])
    return goals


def cost(foods, foods_used):
    """Helper function that calculates the cost of foods used.

    Args:
        foods: A list of foods to reference for costs
        foods_used: A dictionary of indices mapping to counts

    Returns:
        A value representing the cost
    """
    cost = 0.00
    for i, count in foods_used.items():
        cost += (foods[i]['serving_cost'] * count)
    return cost


def calories(foods, foods_used):
    """Helper function that calculates the calories of foods used.

    Args:
        foods: A list of foods to reference for calories
        foods_used: A dictionary of indices mapping to counts

    Returns:
        A value representing the calories
    """
    calories = 0.0
    for i, count in foods_used.items():
        calories += (foods[i]['calories'] * count)
    return calories


def protein(foods, foods_used):
    """Helper function that calculates the protein of foods used.

    Args:
        foods: A list of foods to reference for protein
        foods_used: A dictionary of indices mapping to counts

    Returns:
        A value representing the protein
    """
    protein = 0.0
    for i, count in foods_used.items():
        protein += (foods[i]['protein'] * count)
    return protein


def carbs(foods, foods_used):
    """Helper function that calculates the carbs of foods used.

    Args:
        foods: A list of foods to reference for carbs
        foods_used: A dictionary of indices mapping to counts

    Returns:
        A value representing the carbs
    """
    carbs = 0.0
    for i, count in foods_used.items():
        carbs += (foods[i]['carbs'] * count)
    return carbs


def fat(foods, foods_used):
    """Helper function that calculates the fat of foods used.

    Args:
        foods: A list of foods to reference for fat
        foods_used: A dictionary of indices mapping to counts

    Returns:
        A value representing the fat
    """
    fat = 0.0
    for i, count in foods_used.items():
        fat += (foods[i]['fat'] * count)
    return fat


def init_one_d_array(len, val):
    """Returns an initialized array of a given length where
    all values are equal to the given value.

    Args:
        len: A length for the array
        val: A value to put at each index of the array

    Returns:
        An initialized array
    """
    return [val for i in range(len)]


def init_two_d_array(dimens, val):
    """Returns an initialized 2D array of a given length
    where all values are equal to the given value.

    Args:
        dimens: A tuple containing the dimensions for the array
        val: A value to put at each index of the array

    Returns:
        An initialized 2D array
    """
    w, x = dimens
    return [[val for j in range(x)] for i in range(w)]


def init_three_d_array(dimens, val):
    """Returns an initialized 3D array of a given length
    where all values are equal to the given value.

    Args:
        dimens: A tuple containing the dimensions for the array
        val: A value to put at each index of the array

    Returns:
        An initialized 3D array
    """
    w, x, y = dimens
    return [[[val for k in range(y)] for j in range(x)] for i in range(w)]


def init_four_d_array(dimens, val):
    """Returns an initialized 4D array of a given length
    where all values are equal to the given value.

    Args:
        dimens: A tuple containing the dimensions for the array
        val: A value to put at each index of the array

    Returns:
        An initialized 4D array
    """
    w, x, y, z = dimens
    return [[[[val for l in range(z)]
              for k in range(y)]
             for j in range(x)]
            for i in range(w)]


def brute_force_calories_only(foods, done_count, calories_left):
    """Brute forces a set of cheapest foods based on only the caloric
    requirements.

    Intended as a stepping stone along the way to all macros.

    Args:
        foods: A list of food dictionaries
        done_count: A value representing how many foods are 'done'
            being used by the algorithm. i.e. this is a value to track
            the index for the foods list
        calories_left: A float with the amount of calories left for
            which to account

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    if calories_left < 50:  # using a tolerance of 50 calories
        return {}

    if len(foods) <= done_count:  # done going through all the foods
        return {0: 999999}

    # calculate for scenario where you ignore the current food and don't use it
    foods_used_a = brute_force_calories_only(
        foods, done_count + 1, calories_left)
    # calculate for scenario where you use the current food
    if (calories_left - foods[done_count]['calories']) < -50:
        return foods_used_a
    foods_used_b = brute_force_calories_only(
        foods, done_count, calories_left - foods[done_count]['calories'])
    try:
        foods_used_b[done_count] += 1
    except KeyError:
        foods_used_b[done_count] = 1

    if cost(foods, foods_used_a) > cost(foods, foods_used_b):
        return foods_used_b
    return foods_used_a


def brute_force_cal_and_pro_only(foods, done_count, cal_left, pro_left):
    """Brute forces a set of cheapest foods based on only the caloric
    and protein requirements.

    Intended as a stepping stone along the way to all macros.

    Args:
        foods: A list of food dictionaries
        done_count: A value representing how many foods are 'done'
            being used by the algorithm. i.e. this is a value to track
            the index for the foods list
        cal_left: A float with the amount of calories left for which to
            account
        pro_left: A float with the amount of protein left for which to
            account

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    if cal_left < 50 and pro_left < 5:  # using a tolerance of 50 cal/5 pro
        return {}

    if len(foods) <= done_count:  # done going through all the foods
        return {0: 999999}  # this sucks, try to fix it

    # calculate for scenario where you ignore the current food and don't use it
    foods_used_a = brute_force_cal_and_pro_only(
        foods, done_count + 1, cal_left, pro_left)
    # calculate for scenario where you use the current food
    if ((cal_left - foods[done_count]['calories']) < -50
            or (pro_left - foods[done_count]['protein']) < -15):
        return foods_used_a
    foods_used_b = brute_force_cal_and_pro_only(
        foods, done_count, cal_left - foods[done_count]['calories'],
        pro_left - foods[done_count]['protein'])
    try:
        foods_used_b[done_count] += 1
    except KeyError:
        foods_used_b[done_count] = 1

    if cost(foods, foods_used_a) > cost(foods, foods_used_b):
        return foods_used_b
    return foods_used_a


def brute_force_all(foods, done_count, cal_left, pro_left, fat_left, carb_left):
    """Brute forces a set of cheapest foods based on the provided macro
    requirements.

    Args:
        foods: A list of food dictionaries
        done_count: A value representing how many foods are 'done'
            being used by the algorithm. i.e. this is a value to track
            the index for the foods list
        cal_left: A float with the amount of calories left for which to
            account
        pro_left: A float with the amount of protein left for which to
            account

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    # using a tolerance of 50 cal/5 carb/fat/pro
    if cal_left < 50 and pro_left < 5 and fat_left < 5 and carb_left < 5:
        return {}

    if len(foods) <= done_count:  # done going through all the foods
        return {0: 9999999}

    # calculate scenario where you don't use the current food
    foods_used_a = brute_force_all(
        foods, done_count + 1, cal_left, pro_left, fat_left, carb_left)

    # if current food violates reqs, then don't bother calculating for it
    if ((cal_left - foods[done_count]['calories']) < -50
            or (pro_left - foods[done_count]['protein']) < -5
            or (fat_left - foods[done_count]['fat']) < -5
            or (carb_left - foods[done_count]['carbs']) < -5):
        return foods_used_a

    # calculate scenario where you use the current food
    foods_used_b = brute_force_all(
        foods, done_count, cal_left - foods[done_count]['calories'],
        pro_left - foods[done_count]['protein'],
        fat_left - foods[done_count]['fat'],
        carb_left - foods[done_count]['carbs'])
    try:
        foods_used_b[done_count] += 1
    except KeyError:
        foods_used_b[done_count] = 1

    if len(foods_used_b) == 0:
        return foods_used_a

    # calculate cheapest and return
    if cost(foods, foods_used_a) > cost(foods, foods_used_b):
        return foods_used_b
    return foods_used_a


def dp_all_td(foods, done_count, cal_left, pro_left, fat_left, carb_left):
    """A top-down Dynamic Programming algorithm for figuring out the
    cheapest set of foods to satisfy the given macronotrient goals.

    Args:
        foods: A list of food dictionaries
        cal_left: A number representing the calories left
        pro_left: A number representing the protein left
        fat_left: A number representing the fat left
        carb_left: A number representing the carb left
        dp: An initialized-to-{} 5D array with dimens
            (len(foods), cal_goal, pro_goal, carb_goal, fat_goal)

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    # using a tolerance of 50 cal/5 carb/fat/pro
    if cal_left < 50 and pro_left < 5 and fat_left < 5 and carb_left < 5:
        return {}

    # done going through all the foods
    if len(foods) <= done_count:
        return {0: 9999999}

    # need everything in ints for data struct
    cal_left = int(cal_left)
    pro_left = int(pro_left)
    fat_left = int(fat_left)
    carb_left = int(carb_left)

    # try to use solution already calculated
    try:
        foods_used_a = \
            dp[(str(done_count + 1) + '-'
               + str(cal_left) + '-'
               +  str(pro_left) + '-'
               + str(fat_left) + '-'
               + str(carb_left))]
    except KeyError:
        # calculate scenario where you don't use current food
        foods_used_a = dp_all_td(
            foods, done_count + 1, cal_left, pro_left, fat_left, carb_left)

    # if current food violates reqs, then don't bother calc-ing using it
    if ((cal_left - foods[done_count]['calories']) < -50
            or (pro_left - foods[done_count]['protein']) < -5
            or (fat_left - foods[done_count]['fat']) < -5
            or (carb_left - foods[done_count]['carbs']) < -5):
        return foods_used_a

    # try to use solution already calculated
    try:
        foods_used_b = \
            dp[(str(done_count) + '-'
                + str(cal_left - foods[done_count]['calories']) + '-'
                + str(pro_left - foods[done_count]['protein']) + '-'
                + str(fat_left - foods[done_count]['fat']) + '-'
                + str(carb_left - foods[done_count]['carbs']))]
    except KeyError:
        # calculate for scenario where you use the current food
        foods_used_b = dp_all_td(
            foods,
            done_count,
            cal_left - foods[done_count]['calories'],
            pro_left - foods[done_count]['protein'],
            fat_left - foods[done_count]['fat'],
            carb_left - foods[done_count]['carbs'])
    try:
        foods_used_b[done_count] += 1
    except KeyError:
        foods_used_b[done_count] = 1

    # store cheapest, then return it
    if cost(foods, foods_used_a) > cost(foods, foods_used_b):
        dp[(str(done_count) + '-'
            + str(cal_left) + '-'
            + str(pro_left) + '-'
            + str(fat_left) + '-'
            + str(carb_left))] = foods_used_b
        return foods_used_b
    dp[(str(done_count) + '-'
        + str(cal_left) + '-'
        + str(pro_left) + '-'
        + str(fat_left) + '-'
        + str(carb_left))] = foods_used_a
    return foods_used_a


def dp_calories_only(foods, cal_goal):
    """A Dynamic Programming algorithm for figuring out the cheapest
    set of foods to satisfy the given calorie goal.

    Intended as a stepping stone to a DP solution involving all macros

    Args:
        foods: A list of food dictionaries
        cal_goal: A number representing the calorie goal

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    macros = init_one_d_array(cal_goal, 999999999)
    foods_used = init_one_d_array(cal_goal, {})
    for i in range(cal_goal):
        for j in range(len(foods)):
            food = foods[j]
            if int(food['calories']) <= i:
                if macros[i - int(food['calories'])] == 999999999:
                    prev_cost = 0
                    prev_foods_used = {}
                else:
                    prev_cost = macros[i - int(food['calories'])]
                    prev_foods_used = foods_used[i -
                                                 int(food['calories'])].copy()
                if macros[i] > prev_cost + food['serving_cost']:
                    macros[i] = prev_cost + food['serving_cost']
                    try:
                        prev_foods_used[j] += 1
                    except KeyError:
                        prev_foods_used[j] = 1
                    foods_used[i] = prev_foods_used
    return foods_used[cal_goal - 1]


def dp_cal_and_pro_only(foods, cal_goal, pro_goal):
    """A Dynamic Programming algorithm for figuring out the cheapest
    set of foods to satisfy the given calorie and protein goal.

    Intended as a stepping stone to a DP solution involving all macros

    Args:
        foods: A list of food dictionaries
        cal_goal: A number representing the calorie goal
        pro_goal: A number representing the protein goal

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    macros = init_two_d_array((cal_goal, pro_goal), 999999999)
    foods_used = init_two_d_array((cal_goal, pro_goal), {})

    for i in range(cal_goal):
        for j in range(pro_goal):
            for n in range(len(foods)):
                food = foods[n]
                if (int(food['calories']) > i and int(food['protein']) > j):
                    continue
                if (macros[i - int(food['calories'])]
                          [j - int(food['protein'])]
                        == 999999999):
                    prev_cost = 0
                    prev_foods_used = {}
                else:
                    prev_cost = (macros[i - int(food['calories'])]
                                       [j - int(food['protein'])])
                    prev_foods_used = \
                        (foods_used[i - int(food['calories'])]
                                   [j - int(food['protein'])]).copy()
                new_cal = calories(foods, prev_foods_used) + food['calories']
                new_pro = protein(foods, prev_foods_used) + food['protein']
                if (macros[i][j] > prev_cost + food['serving_cost']
                    and new_cal > i - 50 and new_cal < i + 10
                    and new_pro > j - 5 and new_pro < j + 5):
                    macros[i][j] = prev_cost + food['serving_cost']
                    try:
                        prev_foods_used[n] += 1
                    except KeyError:
                        prev_foods_used[n] = 1
                    foods_used[i][j] = prev_foods_used
    return foods_used[cal_goal - 1][pro_goal - 1]


def dp_all(foods, cal_goal, pro_goal, carb_goal, fat_goal):
    """A bottom-up Dynamic Programming algorithm for figuring out the
    cheapest set of foods to satisfy the given macronotrient goals.

    Args:
        foods: A list of food dictionaries
        cal_goal: A number representing the calorie goal
        pro_goal: A number representing the protein goal

    Returns:
        Dictionary mapping indices of foods used in the final solution
        to their respective counts
    """
    costs = init_four_d_array((cal_goal, pro_goal, carb_goal, fat_goal),
                              999999999)
    foods_used = init_four_d_array((cal_goal, pro_goal, carb_goal, fat_goal),
                                   {})

    for i in range(cal_goal):
        for j in range(pro_goal):
            for k in range(carb_goal):
                for l in range(fat_goal):
                    for n in range(len(foods)):
                        food = foods[n]
                        if (int(food['calories']) > i
                            or int(food['protein']) > j
                            or int(food['carbs']) > k
                                or int(food['fat']) > l):
                            continue
                        if (costs[i - int(food['calories'])]
                                 [j - int(food['protein'])]
                                 [k - int(food['carbs'])]
                                 [l - int(food['fat'])]
                                == 999999999):
                            prev_cost = 0
                            prev_foods_used = {}
                        else:
                            prev_cost = (macros[i - int(food['calories'])]
                                               [j - int(food['protein'])]
                                               [j - int(food['carbs'])]
                                               [j - int(food['fat'])])
                            prev_foods_used = \
                                (foods_used[i - int(food['calories'])]
                                           [j - int(food['protein'])]
                                           [k - int(food['carbs'])]
                                           [l - int(food['fat'])]).copy()
                        new_cal = calories(
                            foods, prev_foods_used) + food['calories']
                        new_pro = protein(
                            foods, prev_foods_used) + food['protein']
                        new_car = carbs(
                            foods, prev_foods_used) + food['protein']
                        new_fat = fat(
                            foods, prev_foods_used) + food['protein']
                        if (costs[i][j] > prev_cost + food['serving_cost']
                            and new_cal > i - 20 and new_cal < i + 10
                            and new_pro < j + 5 and new_pro < j + 5
                            and new_car < j + 5 and new_car < j + 5
                            and new_fat < j + 5 and new_fat < j + 5):
                            costs[i][j][k][l] = prev_cost + \
                                food['serving_cost']
                            try:
                                prev_foods_used[n] += 1
                            except KeyError:
                                prev_foods_used[n] = 1
                            foods_used[i][j][k][l] = prev_foods_used
    return foods_used[cal_goal - 1][pro_goal - 1][carb_goal - 1][fat_goal - 1]


def main():
    """Main wrapper."""
    args = parser.parse_args()

    foods = build_foods(args.foods[0])
    goals = build_goals(args.goals[0])

    print('GOALS:')
    for macro in sorted(goals.keys()):
        print(' -> {}: {}'.format(macro, int(goals[macro])))

    # print('==========================================')
    # print('DYNAMIC PROGRAMMING, CALORIES ONLY')
    # t = time.process_time()
    # foods_used = dp_calories_only(foods, int(goals['calories']))
    # elapsed = time.process_time() - t
    # print('Performance: {0:.4f} s'.format(elapsed))
    # print('---------')
    # print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    # print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    # print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    # print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    # print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    # print('Using:')
    # for i, count in foods_used.items():
    #     print(' -> {}: {} x {}'.format(foods[i]['name'], count,
    #                                    foods[i]['serving_size']))
    #
    # print('==========================================')
    # print('BRUTE FORCE, CALORIES ONLY')
    # t = time.process_time()
    # foods_used = brute_force_calories_only(foods, 0, goals['calories'])
    # elapsed = time.process_time() - t
    # print('Performance: {0:.4f} s'.format(elapsed))
    # print('---------')
    # print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    # print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    # print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    # print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    # print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    # print('Using:')
    # for i, count in foods_used.items():
    #     print(' -> {}: {} x {}'.format(foods[i]['name'], count,
    #                                    foods[i]['serving_size']))
    #
    # print('==========================================')
    # print('DYNAMIC PROGRAMMING, CALORIES AND PROTEIN ONLY')
    # t = time.process_time()
    # foods_used = dp_cal_and_pro_only(
    #     foods, int(goals['calories']), int(goals['protein']))
    # elapsed = time.process_time() - t
    # saved_elapsed = elapsed
    # print('Performance: {0:.4f} s'.format(elapsed))
    # print('---------')
    # print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    # print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    # print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    # print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    # print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    # print('Using:')
    # for i, count in foods_used.items():
    #     print(' -> {}: {} x {}'.format(foods[i]['name'], count,
    #                                    foods[i]['serving_size']))
    #
    # print('==========================================')
    # print('BRUTE FORCE, CALORIES AND PROTEIN ONLY')
    # t = time.process_time()
    # foods_used = brute_force_cal_and_pro_only(
    #     foods, 0, goals['calories'], goals['protein'])
    # elapsed = time.process_time() - t
    # print('Performance: {0:.4f} s'.format(elapsed))
    # print('---------')
    # print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    # print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    # print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    # print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    # print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    # print('Using:')
    # for i, count in foods_used.items():
    #     print(' -> {}: {} x {}'.format(foods[i]['name'], count,
    #                                    foods[i]['serving_size']))

    # print('==========================================')
    # print('DYNAMIC PROGRAMMING, ALL MACROS')
    # t = time.process_time()
    # foods_used = dp_all(
    #     foods, int(goals['calories']), int(goals['protein']),
    #     int(goals['carbs']), int(goals['fat']))
    # elapsed = time.process_time() - t
    # print('Performance: {0:.4f} s'.format(elapsed))
    # print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    # print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    # print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    # print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    # print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    # print('Using:')
    # for i, count in foods_used.items():
    #     print(' -> {}: {} x {}'.format(foods[i]['name'], count,
    #                                    foods[i]['serving_size']))

    print('==========================================')
    print('BRUTE FORCE, ALL MACROS')
    t = time.process_time()
    foods_used = brute_force_all(
        foods, 0, goals['calories'], goals['protein'], goals['fat'],
        goals['carbs'])
    elapsed = time.process_time() - t
    print('Performance: {0:.4f} s'.format(elapsed))
    print('---------')
    print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    print('Using:')
    for i, count in foods_used.items():
        print(' -> {}: {} x {}'.format(foods[i]['name'], count,
                                       foods[i]['serving_size']))

    print('==========================================')
    print('DYNAMIC PROGRAMMING (TOP-DOWN), ALL MACROS')
    t = time.process_time()
    foods_used = dp_all_td(
        foods, 0, goals['calories'], goals['protein'], goals['fat'],
        goals['carbs'])
    elapsed = time.process_time() - t
    print('Performance: {0:.4f} s'.format(elapsed))
    print('---------')
    print('Cost:     ${0:.2f}'.format(cost(foods, foods_used)))
    print('Calories: {} cal'.format(int(calories(foods, foods_used))))
    print('Protein:  {} g'.format(int(protein(foods, foods_used))))
    print('Carbs:    {} g'.format(int(carbs(foods, foods_used))))
    print('Fat:      {} g'.format(int(fat(foods, foods_used))))
    print('Using:')
    for i, count in foods_used.items():
        print(' -> {}: {} x {}'.format(foods[i]['name'], count,
                                       foods[i]['serving_size']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Calculates cheapest way to satisfy macro requirements.')
    parser.add_argument('--foods', nargs=1, required=True,
                        help='File containing food info')
    parser.add_argument('--goals', nargs=1, required=True,
                        help='File containing goal info')
    main()
