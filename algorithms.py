import datetime

import math
import random

import numpy as np

import functions as fc
import dataexports as de


def create_filled_random_list(dimension, items_per_category):
    random_list = list()
    for _ in range(dimension):
        random_list.append(random.randint(0, items_per_category - 1))
    return random_list


def knapsack_cost_function(list_of_values_and_weights_tuples, weight_limit):
    res = float(0)
    total_weight = 0
    for i in range(len(list_of_values_and_weights_tuples)):
        total_weight += list_of_values_and_weights_tuples[i][1]
        if total_weight > weight_limit:
            return 0
        res += list_of_values_and_weights_tuples[i][0]
    return res


def get_solution_prices_and_weights_tuple_list(solution, items_per_category, all_item_values_and_weights_tuples):
    solution_prices_and_weights_tuples = list()
    for i in range(len(solution)):
        index = i * items_per_category + solution[i]
        solution_prices_and_weights_tuples.append(all_item_values_and_weights_tuples[index])
    return solution_prices_and_weights_tuples


def bruteforce(item_values_and_weights_tuples, weight_limit, dimension, items_per_category):
    best_solution = list()
    best_solution_prices = list()
    best_solution_weights = list()
    best_solution_score = 0
    total_solution_count = pow(items_per_category, dimension)
    current_solution = list()
    # convergence_list = list()
    start_timestamp = datetime.datetime.now()

    for _ in range(dimension):
        current_solution.append(0)

    for count in range(total_solution_count):
        solution_prices_and_weights_tuples = get_solution_prices_and_weights_tuple_list(current_solution,
                                                                                        items_per_category,
                                                                                        item_values_and_weights_tuples)
        current_score = knapsack_cost_function(solution_prices_and_weights_tuples, weight_limit)
        if current_score > best_solution_score:
            best_solution_score = current_score
            best_solution.clear()
            for bsi in range(dimension):
                best_solution.append(current_solution[bsi])
            best_solution_prices.clear()
            best_solution_weights.clear()
            for p in range(dimension):
                best_solution_prices.append(solution_prices_and_weights_tuples[p][0])
                best_solution_weights.append(solution_prices_and_weights_tuples[p][1])

        # convergence_list.append(best_solution_score)
        current_solution = shift_solution_by_one(current_solution, len(current_solution) - 1, items_per_category)
    end_timestamp = datetime.datetime.now()

    de.write_solution_file(f"./output/BF_solution_d{dimension}.csv", best_solution, best_solution_prices,
                           best_solution_weights, start_timestamp, end_timestamp)
    # de.plot_and_save_single_line("./output", f"BF_timeline_d{dimension}.png",
    # f"Bruteforce best solution timeline for {dimension} classes",
    # "Iterations", "CF Value", convergence_list)
    return 0


def shift_solution_by_one(original_solution, shift_at_index, value_limit):
    if shift_at_index < 0:
        return list()
    if original_solution[shift_at_index] + 1 < value_limit:
        original_solution[shift_at_index] += 1
        return original_solution
    original_solution[shift_at_index] = 0
    return shift_solution_by_one(original_solution, shift_at_index - 1, value_limit)


def simulated_annealing(primary_loop_iterations, metropolis_repetitions,
                        dimension, items_per_category, item_values_and_weights_tuples, weight_limit,
                        starting_temperature, min_temperature, cooling_rate):
    very_best_result = float(0)
    very_best_solution = list()
    convergence_list = list()
    best_solution_prices = list()
    best_solution_weights = list()
    temperature = starting_temperature
    start_timestamp = datetime.datetime.now()
    for x in range(primary_loop_iterations):
        centerpoint_solution = create_filled_random_list(dimension, items_per_category)
        solution_prices_and_weights_tuples = get_solution_prices_and_weights_tuple_list(centerpoint_solution,
                                                                                        items_per_category,
                                                                                        item_values_and_weights_tuples)
        metropolis_best_result = knapsack_cost_function(solution_prices_and_weights_tuples, weight_limit)
        for i in range(1, metropolis_repetitions + 1):
            new_solution = get_neighbour_solution(centerpoint_solution, dimension, items_per_category)
            new_prices_and_weights_tuples = get_solution_prices_and_weights_tuple_list(centerpoint_solution,
                                                                                       items_per_category,
                                                                                       item_values_and_weights_tuples)
            new_result = knapsack_cost_function(new_prices_and_weights_tuples, weight_limit)
            if new_result > metropolis_best_result:
                metropolis_best_result = new_result
                centerpoint_solution.clear()
                for nsi in range(dimension):
                    centerpoint_solution.append(new_solution[nsi])
            else:
                chance_to_keep_previous = np.random.uniform(0, 1)
                difference = metropolis_best_result - new_result
                if chance_to_keep_previous < math.exp(-difference / temperature):
                    metropolis_best_result = new_result
                    centerpoint_solution.clear()
                    for nsi in range(dimension):
                        centerpoint_solution.append(new_solution[nsi])
            if metropolis_best_result > very_best_result:
                very_best_result = metropolis_best_result
                very_best_solution.clear()
                for bsi in range(dimension):
                    very_best_solution.append(new_solution[bsi])
                best_solution_prices.clear()
                best_solution_weights.clear()
                for p in range(dimension):
                    best_solution_prices.append(new_prices_and_weights_tuples[p][0])
                    best_solution_weights.append(new_prices_and_weights_tuples[p][1])
            convergence_list.append(very_best_result)
        if temperature * cooling_rate >= min_temperature:
            temperature *= cooling_rate
    end_timestamp = datetime.datetime.now()
    de.write_solution_file(f"./output/SA_solution_d{dimension}.csv", very_best_solution, best_solution_prices,
                           best_solution_weights, start_timestamp, end_timestamp)
    return convergence_list


def get_neighbour_solution(centerpoint, dimension, items_per_category):
    new_solution = list()
    changing_index = random.randint(0, dimension - 1)
    changing_direction = random.randint(0, 1)
    if changing_direction == 1:
        new_value = centerpoint[changing_index] + 1
        if new_value >= items_per_category:
            new_value = 0
    else:
        new_value = centerpoint[changing_index] - 1
        if new_value < 0:
            new_value = items_per_category - 1
    for i in range(len(centerpoint)):
        new_solution.append(centerpoint[i])
    new_solution[changing_index] = new_value
    return new_solution
