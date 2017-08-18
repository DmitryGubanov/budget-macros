#!/usr/bin/python

import argparse
import time


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


def brute_force_calories_only(foods, done_count, calories_left):
    """Brute forces a set of cheapest foods based on only the caloric
    requirements.

    Intended as a stepping stone along the way to the DP solution.

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

    Intended as a stepping stone along the way to the DP solution.

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

    Intended as a stepping stone along the way to the DP solution.

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
    # using a tolerance of 50 cal/5 pro
    if cal_left < 50 and pro_left < 5 and fat_left < 5 and carb_left < 5:
        return {}

    if len(foods) <= done_count:  # done going through all the foods
        return {0: 999999}  # this sucks, try to fix it

    # calculate for scenario where you ignore the current food and don't use it
    foods_used_a = brute_force_all(
        foods, done_count + 1, cal_left, pro_left, fat_left, carb_left)
    # calculate for scenario where you use the current food
    if ((cal_left - foods[done_count]['calories']) < -50
            or (pro_left - foods[done_count]['protein']) < -15
            or (fat_left - foods[done_count]['fat']) < -10
            or (carb_left - foods[done_count]['carbs']) < -10):
        return foods_used_a
    foods_used_b = brute_force_all(
        foods, done_count, cal_left - foods[done_count]['calories'],
        pro_left - foods[done_count]['protein'],
        fat_left - foods[done_count]['fat'],
        carb_left - foods[done_count]['carbs'])
    try:
        foods_used_b[done_count] += 1
    except KeyError:
        foods_used_b[done_count] = 1

    if cost(foods, foods_used_a) > cost(foods, foods_used_b):
        return foods_used_b
    return foods_used_a


def main():
    """Main wrapper."""
    args = parser.parse_args()

    foods = build_foods(args.foods[0])
    goals = build_goals(args.goals[0])
    # print(foods)
    # print(goals)

    print('GOALS:')
    for macro in sorted(goals.keys()):
        print(' -> {}: {}'.format(macro, int(goals[macro])))

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Calculates cheapest way to satisfy macro requirements.')
    parser.add_argument('--foods', nargs=1, help='File containing food info')
    parser.add_argument('--goals', nargs=1, help='File containing goal info')
    main()
