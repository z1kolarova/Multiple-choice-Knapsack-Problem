from pathlib import Path

import algorithms as al
import dataexports as de

category_count = 11
items_per_category = 3
backpack_capacity = 300

total_solution_count = pow(items_per_category, category_count)

runs = 30

sa_main_iterations = min(int(total_solution_count / items_per_category / category_count), 100)
sa_metropolis_iterations = category_count
sa_start_temp = 1200
sa_min_temp = 0.1
sa_cooling_rate = 0.94

"""while category_count < 25:
    catalogue_filename = f"item_catalogue_c{category_count}.csv"
    dirname = "./output/"
    full_catalogue_path = f"{dirname}{catalogue_filename}"
    de.directory_preparation(dirname)

    catalogue_exists = Path(full_catalogue_path).is_file()
    #if not catalogue_exists:

    viability_check = 301
    while viability_check > 300:
        viability_check = 0
        de.generate_item_catalogue(dirname, catalogue_filename, category_count, items_per_category)
        items = de.load_from_item_catalogue(full_catalogue_path)
        for i in range(category_count):
            start_index = i * items_per_category
            smallest_weight_in_category = items[start_index].weight
            for j in range(items_per_category - 1):
                current_weight = items[start_index + 1 + j].weight
                if current_weight < smallest_weight_in_category:
                    smallest_weight_in_category = current_weight
            viability_check += smallest_weight_in_category

    values_and_weights_tuple_list = de.convert_item_list_to_values_and_weights_tuple_list(items)
    al.bruteforce(values_and_weights_tuple_list, backpack_capacity, category_count, items_per_category)
    category_count += 1"""

catalogue_filename = f"item_catalogue_c{category_count}.csv"
dirname = "./output/"
filenamebase = f"SA_timeline_d{category_count}"
titlebase = f"Simulated annealing on MCKP with dimension {category_count}"
full_catalogue_path = f"{dirname}{catalogue_filename}"
items = de.load_from_item_catalogue(full_catalogue_path)
values_and_weights_tuple_list = de.convert_item_list_to_values_and_weights_tuple_list(items)

convergences = list()
final_results = list()
averages = list()

de.process_multiple_sa_runs(runs, sa_main_iterations * sa_metropolis_iterations, category_count, items_per_category,
                            backpack_capacity, values_and_weights_tuple_list,
                             convergences, final_results, averages,
                             dirname, filenamebase, titlebase, "", sa_main_iterations,
                             sa_metropolis_iterations, sa_start_temp, sa_min_temp, sa_cooling_rate)
"""sa_convergence = al.simulated_annealing(sa_main_iterations, sa_metropolis_iterations,
                                        category_count, items_per_category, values_and_weights_tuple_list,
                                        backpack_capacity, sa_start_temp, sa_min_temp, sa_cooling_rate)"""

