import random
from enum import Enum
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import algorithms as al


class Item(object):
    def __init__(self, category, id_in_category, price, weight):
        self.category = category
        self.id_in_category = id_in_category
        self.price = price
        self.weight = weight

    @staticmethod
    def header():
        return "CATEGORY;ID IN CATEGORY;PRICE;WEIGHT\n"

    def data_row(self):
        return f"{self.category};{self.id_in_category};{self.price};{self.weight}\n"

    @staticmethod
    def footer(price_sum, weight_sum):
        return f"TOTAL PRICE;{price_sum};TOTAL WEIGHT;{weight_sum}\n"


def directory_preparation(dirname):
    Path(f"./{dirname}").mkdir(parents=True, exist_ok=True)


def generate_item_catalogue(dir_path, filename, category_count, items_per_category):
    low_border = 1
    up_border = 50
    price_sum = 0
    weight_sum = 0
    full_file_path = f"{dir_path}/{filename}"
    file = open(full_file_path, "a")
    file.write(Item.header())
    for category in range(1, category_count + 1):
        for item_id in range(1, items_per_category + 1):
            price = random.randint(low_border, up_border)
            weight = random.randint(low_border, up_border)
            file.write(Item.data_row(Item(category, item_id, price, weight)))
            price_sum += price
            weight_sum += weight
    file.write(Item.footer(price_sum, weight_sum))


def load_from_item_catalogue(full_file_path):
    items = list()
    with open(full_file_path) as file:
        for line in file:
            line_content = line.rstrip()
            line_segments = line_content.split(";")
            if not line_segments[0].isnumeric():
                continue
            items.append(Item(int(line_segments[0]), int(line_segments[1]), int(line_segments[2]),
                              int(line_segments[3])))
    return items


def convert_item_list_to_values_and_weights_tuple_list(items):
    values_and_weights_tuple_list = list()
    for i in range(len(items)):
        item = items[i]
        values_and_weights_tuple_list.append((item.price, item.weight))
    return values_and_weights_tuple_list


def write_solution_file(full_file_path, ids, prices, weights, timestamp_start, timestamp_end):
    price_sum = 0
    weight_sum = 0
    file = open(full_file_path, "a")
    file.write(Item.header())
    for record_id in range(len(ids)):
        file.write(Item.data_row(Item(record_id + 1, ids[record_id] + 1, prices[record_id], weights[record_id])))
        price_sum += prices[record_id]
        weight_sum += weights[record_id]
    file.write(Item.footer(price_sum, weight_sum))
    file.write(f"Calculations began;{timestamp_start};Calculations ended;{timestamp_end}\n")


def plot_and_save_single_line(dir_path, filename, title, x_label, y_label, y_values):
    x_points = range(1, len(y_values) + 1)
    y_points = np.asarray(y_values)
    plt.plot(x_points, y_points)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(f"{dir_path}/{filename}", bbox_inches='tight')
    plt.close()


def plot_and_save_many_lines(dir_path, filename, title, x_label, x_point_count, y_label, list_of_lists_with_y_values):
    x_points = range(1, x_point_count + 1)
    for result in list_of_lists_with_y_values:
        plt.plot(x_points, np.asarray(result))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(f"./{dir_path}/{filename}", bbox_inches='tight')
    plt.close()


def plot_and_save_multiple_lines_with_legend(dir_path, filename, title, x_label, x_point_count, y_label,
                                             y_set_and_name_tuple_list):
    x_points = range(1, x_point_count + 1)
    for result in y_set_and_name_tuple_list:
        plt.plot(x_points, np.asarray(result[0]), label=result[1])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.savefig(f"./{dir_path}/{filename}", bbox_inches='tight')
    plt.close()


def process_multiple_sa_runs(runs, iterations, dimension, items_per_category, backpack_capacity,
                             values_and_weights_tuple_list,
                             convergences, final_results, averages,
                             dirname, filenamebase, titlebase, statistics_filename, sa_primary_iterations,
                             sa_metropolis_iterations, sa_start_temp, sa_min_temp, sa_cooling_rate):
    for i in range(runs):
        convergence_of_run = al.simulated_annealing(sa_primary_iterations, sa_metropolis_iterations,
                                                    dimension, items_per_category, values_and_weights_tuple_list,
                                                    backpack_capacity, sa_start_temp, sa_min_temp, sa_cooling_rate)
        convergences.append(convergence_of_run)
        """de.save_plotted("./output/", f"{i}.png", titlebase, "Iterations", "CF Value", convergence_of_run)"""
        final_results.append(convergence_of_run[iterations - 1])
    average_helper = list()
    for j in range(iterations):
        average_helper.clear()
        for k in range(runs):
            average_helper.append(convergences[k][j])
        averages.append(np.average(average_helper))

    plot_and_save_single_line(dirname, f"{filenamebase}_average.png",
                              f"Average best solution timeline for {dimension} classes",
                              "Iterations", "CF Value", averages)
    plot_and_save_many_lines(dirname, f"{filenamebase}.png",
                             f"{titlebase} - Evolution of CF Value for all solutions ",
                             "Iterations", iterations, "CF Value", convergences)

    """csv_data = Statistics(filenamebase, min(final_results), max(final_results),
                          np.mean(final_results),
                          np.median(final_results), np.std(final_results))
    statistics_csv(statistics_filename, csv_data)"""