import numpy as np
import os
import matplotlib.pyplot as plt


def plot_losses_time_dep(output_folder, time, populations, filename_base):

    plt.figure(figsize=(10, 6))
    num_populations = populations.shape[0]

    if num_populations > 0:
        labels = ["Holes", "Electrons Zone 1", "Electrons Zone 2"] 
        for i in range(num_populations):
            label = labels[i] if i < len(labels) else f'Population {i+1}'
            plt.plot(time, populations[i], label=label)
    else:
        print("No population data to plot.")
        plt.text(0.5, 0.5, 'No population data found', horizontalalignment='center', verticalalignment='center')

    plt.xlabel("Time (fs)") 
    plt.ylabel("Population (sum over k)")
    plt.title("Population Dynamics") 
    if num_populations > 0:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()

    os.makedirs(output_folder, exist_ok=True)

    plot_filename = os.path.join(output_folder, f"{filename_base}_Losses.png")
    try:
        plt.savefig(plot_filename)
        print(f"Saved plot: {plot_filename}")
    except Exception as e:
        print(f"Error saving plot {plot_filename}: {e}")
    plt.close()


loss_file_path = r"D:/working harder making better/27_03_hBN_Coulomb/NOCOULOMB_Nk_200intens_0.00e+00_t1_-2.3_dt_0.1/NOCOULOMB_Nk_200intens_0.00e+00_t1_-2.3_dt_0.1_6.00/Output/Losses.txt"

print(f"--- Processing File: {loss_file_path} ---")


try:
    output_dir = os.path.dirname(loss_file_path) 
    scenario_dir = os.path.dirname(output_dir) 
    base_dir = os.path.dirname(scenario_dir) 
    scenario_name = os.path.basename(scenario_dir) 

    picture_folder = os.path.join(base_dir, "pictures_" + scenario_name + "_Losses")
    picture_filename_base = scenario_name 
    print(f"Output picture folder: {picture_folder}")

except Exception as e:
    print(f"Error determining output path: {e}. Saving pictures to current directory.")
    picture_folder = "." 
    picture_filename_base = "Population_Plot"


if os.path.isfile(loss_file_path):
    try:

        data = np.genfromtxt(loss_file_path, unpack=True, skip_header=1, comments='#', invalid_raise=False)

        if data.size == 0 or data.ndim == 0:
             print(f"Warning: Empty or invalid data in {loss_file_path}")
             exit() 

        if data.ndim == 1: 
             print(f"Error: Only one column found in {loss_file_path}. Expected time and populations.")
             exit()
        elif data.shape[0] != 4: 
             print(f"Warning: Expected 4 columns (Time + 3 Populations), but found {data.shape[0]}.")

        time_data = data[0]
        population_data = data[1:]


        if population_data.ndim == 1:
            population_data = population_data.reshape(1, -1)

        print(f"Data loaded. Time points: {len(time_data)}, Population types found: {population_data.shape[0]}")

        plot_losses_time_dep(picture_folder, time_data, population_data, picture_filename_base)

    except Exception as e:
        print(f"Error reading or processing {loss_file_path}: {e}")
        import traceback
        traceback.print_exc() 
else:
    print(f"Error: File not found at {loss_file_path}")

print("\n--- Script Finished ---")
