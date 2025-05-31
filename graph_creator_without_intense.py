import matplotlib.pyplot as plt
import os
import numpy as np
import re # Импортируем модуль для регулярных выражений

# --- КОНФИГУРАЦИЯ ---
# !!! ВАЖНО: Укажите путь к ОСНОВНОЙ ДИРЕКТОРИИ, где лежат все папки ReCalc_... !!!
main_processing_directory = r"D:\working harder making better\27_03_hBN_Coulomb" # <--- ИЗМЕНИТЕ ЭТОТ ПУТЬ

file_w_name = "2p_w_at_zero.txt"
file_abs_name = "2p_Abs_at_zero.txt"

# Шаблон для имен папок. Он будет искать папки, начинающиеся с "ReCalc_UncellArea__..."
# и содержащие "..._Pump_R0-<значение>EPS-<значение>"
# Группы в скобках ( ... ) извлекают значения R0 и EPS
folder_name_pattern = r"^ReCalc_UncellArea__Nk_200intens_0\.00e\+00_t1_-2\.3_Ncut20_qTF_0\.01_dt_0\.1_delayXUV_0w_Pump_R0-([-\d\.]+)EPS-([-\d\.]+)$"
folder_pattern_compiled = re.compile(folder_name_pattern)
# ---------------------

def extract_params_from_path_string(path_string):
    """
    Извлекает параметры R0 и EPS из имени последней папки в пути.
    Эта функция может быть полезна, если шаблон имени папки более сложный,
    или если вы хотите извлечь параметры из уже известного пути.
    """
    folder_name = os.path.basename(path_string)
    r0_value = None
    eps_value = None

    r0_match = re.search(r"R0-([-\d\.]+)", folder_name)
    if r0_match:
        r0_value = r0_match.group(1)

    eps_match = re.search(r"EPS-([-\d\.]+)", folder_name)
    if eps_match:
        eps_value = eps_match.group(1)
    return r0_value, eps_value

def load_data_from_file(filepath):
    data = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                number_strings = line_stripped.split()
                for num_str in number_strings:
                    try:
                        value = float(num_str)
                        data.append(value)
                    except ValueError:
                        print(f"Warning: Could not convert string '{num_str}' to a number in file {filepath}. Value skipped.")
        if not data:
             print(f"Warning: File {filepath} is empty or does not contain valid numerical data after processing.")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at path: {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading file {filepath}: {e}")
        return None

def process_single_folder(current_folder_path, r0_from_name, eps_from_name):
    """
    Обрабатывает данные из одной папки: загружает, строит график и сохраняет его.
    """
    print(f"\n--- Processing folder: {os.path.basename(current_folder_path)} ---")

    path_w = os.path.join(current_folder_path, file_w_name)
    path_abs = os.path.join(current_folder_path, file_abs_name)

    print(f"Loading data for X-axis (frequency w) from file: {path_w}")
    w_data = load_data_from_file(path_w)

    print(f"Loading data for Y-axis (ABS) from file: {path_abs}")
    abs_data = load_data_from_file(path_abs)

    if w_data and abs_data:
        if len(w_data) == len(abs_data):
            print("Data loaded successfully. Plotting graph...")

            w_data_np = np.array(w_data)
            abs_data_np = np.array(abs_data)

            if len(abs_data_np) > 0:
                max_y = np.max(abs_data_np)
                y_threshold = 0.001

                interesting_indices = np.where(abs_data_np > y_threshold)[0]

                if len(interesting_indices) > 0:
                    min_x_interesting = w_data_np[interesting_indices[0]]
                    max_x_interesting = w_data_np[interesting_indices[-1]]

                    x_range_interesting = max_x_interesting - min_x_interesting
                    padding_x = x_range_interesting * 0.2
                    
                    xlim_min = min_x_interesting - padding_x
                    xlim_max = max_x_interesting + padding_x

                    xlim_min = max(xlim_min, np.min(w_data_np))
                    xlim_max = min(xlim_max, np.max(w_data_np))
                    
                    ylim_min = -0.005
                    ylim_max = max_y * 1.1 if max_y > 0 else 0.1 # Handle case where max_y is 0 or negative
                else:
                    print("No significant peaks found based on the threshold. Displaying full range.")
                    xlim_min, xlim_max = np.min(w_data_np), np.max(w_data_np)
                    ylim_min, ylim_max = np.min(abs_data_np), (np.max(abs_data_np) * 1.1 if np.max(abs_data_np) > 0 else 0.1)
            else:
                print("Warning: abs_data_np is empty. Setting default plot limits.")
                xlim_min, xlim_max = 0, 1
                ylim_min, ylim_max = 0, 1


            fig, ax = plt.subplots(figsize=(10, 6)) # Создаем фигуру и оси
            ax.plot(w_data_np, abs_data_np, linestyle='-', linewidth=2, label='ABS(w)')

            ax.set_xlabel("Frequency w")
            ax.set_ylabel("ABS")
            ax.set_title(f"ABS vs. Frequency w (R0={r0_from_name}, EPS={eps_from_name})")
            
            ax.grid(True, which='major', linestyle='-', linewidth=0.8, color='darkgray')
            ax.minorticks_on()
            ax.grid(which='minor', linestyle=':', linewidth=0.5, color='lightgray')

            ax.set_xlim(xlim_min, xlim_max)
            ax.set_ylim(ylim_min, ylim_max)

            ax.legend()

            # --- ФОРМИРОВАНИЕ ИМЕНИ ФАЙЛА ДЛЯ СОХРАНЕНИЯ ---
            output_filename_parts = ["plot_w_vs_abs"]
            if r0_from_name is not None:
                output_filename_parts.append(f"R0_{r0_from_name}")
            if eps_from_name is not None:
                output_filename_parts.append(f"EPS_{eps_from_name}")
            
            output_filename = "_".join(output_filename_parts) + ".png"
            
            output_plot_path = os.path.join(current_folder_path, output_filename)
            plt.savefig(output_plot_path)
            print(f"Plot saved to: {output_plot_path}")

            # plt.show() # Закомментировано для пакетной обработки, чтобы не показывать каждый график
            plt.close(fig) # Закрываем фигуру, чтобы освободить память

        else:
            print(f"Error in folder {os.path.basename(current_folder_path)}: The number of data points in the files does not match!")
            print(f"  File '{file_w_name}' has {len(w_data)} points.")
            print(f"  File '{file_abs_name}' has {len(abs_data)} points.")
            print("The graph cannot be plotted correctly for this folder.")
    else:
        if not w_data:
            print(f"Failed to load data from {file_w_name} in folder {os.path.basename(current_folder_path)} or it was empty/invalid.")
        if not abs_data:
            print(f"Failed to load data from {file_abs_name} in folder {os.path.basename(current_folder_path)} or it was empty/invalid.")
        print(f"The graph will not be plotted for folder {os.path.basename(current_folder_path)}.")


# --- ОСНОВНОЙ БЛОК ВЫПОЛНЕНИЯ ---
if __name__ == "__main__":
    if not os.path.isdir(main_processing_directory):
        print(f"Error: Main processing directory not found: {main_processing_directory}")
        print("Please set the 'main_processing_directory' variable correctly.")
    else:
        print(f"Starting to scan directory: {main_processing_directory}")
        found_matching_folders = 0
        for item_name in os.listdir(main_processing_directory):
            item_path = os.path.join(main_processing_directory, item_name)
            if os.path.isdir(item_path):
                # Проверяем, соответствует ли имя папки нашему шаблону
                match = folder_pattern_compiled.match(item_name)
                if match:
                    found_matching_folders += 1
                    r0_val = match.group(1) # Первое значение в скобках в regex (R0)
                    eps_val = match.group(2) # Второе значение в скобках в regex (EPS)
                    
                    # Вызываем функцию обработки для этой папки
                    process_single_folder(item_path, r0_val, eps_val)
                # else:
                    # print(f"Skipping non-matching directory: {item_name}") # Можно раскомментировать для отладки

        if found_matching_folders == 0:
            print(f"\nNo folders matching the pattern '{folder_name_pattern}' were found in '{main_processing_directory}'.")
            print("Please check the 'main_processing_directory' path and the 'folder_name_pattern'.")
        else:
            print(f"\nSuccessfully processed {found_matching_folders} matching folder(s).")

    print("\nScript finished.")