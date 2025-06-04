import matplotlib.pyplot as plt
import pandas as pd
import os


file_path_str_1 = r"\\?\D:\working harder making better\27_03_hBN_Coulomb\ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0\ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0_6.00\Output\Losses.txt"
file_path_str_2 = r"D:\working harder making better\27_03_hBN_Coulomb\NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1\NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1_6.00\Output\Losses.txt"


x_col_index = 0


y_col_indices = [1, 2, 3] 


y_column_names = [
    "Energy Loss Type 1",  
    "Energy Loss Type 2",  
    "Total Energy Loss"    
]



def load_and_prepare_data(file_path, x_col_idx, y_col_idx, file_label=""):
    """
    Loads data from a specified column in a text file.
    Validates file existence and required number of columns.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at path ({file_label}, Y-col: {y_col_idx+1}): {file_path}")
        return None, None

    try:

        data = pd.read_csv(file_path, delim_whitespace=True, header=None, comment='#')

        if data.empty:
            print(f"Error: File {file_path} ({file_label}, Y-col: {y_col_idx+1}) is empty.")
            return None, None

        required_cols = max(x_col_idx, y_col_idx) + 1
        if data.shape[1] < required_cols:
            print(f"Error for {file_path} ({file_label}, Y-col: {y_col_idx+1}): "
                  f"File has fewer than {required_cols} columns (found {data.shape[1]}). "
                  f"Columns {x_col_idx+1} (for X) and {y_col_idx+1} (for Y) are required.")
            return None, None

        x_values = data.iloc[:, x_col_idx]
        y_values = data.iloc[:, y_col_idx]
        return x_values, y_values

    except pd.errors.EmptyDataError:
        print(f"Error: File {file_path} ({file_label}, Y-col: {y_col_idx+1}) is empty (pd.errors.EmptyDataError).")
        return None, None
    except Exception as e:
        print(f"An error occurred while reading or processing file {file_path} ({file_label}, Y-col: {y_col_idx+1}): {e}")
        return None, None


fig, axs = plt.subplots(len(y_col_indices), 1, figsize=(12, 5 * len(y_col_indices)), sharex=True)
fig.suptitle("Comparison of Data from Losses Files", fontsize=18)


if len(y_col_indices) == 1:
    axs = [axs]

at_least_one_plot_successful = False


for i, y_idx in enumerate(y_col_indices):
    current_y_col_name = y_column_names[i] if i < len(y_column_names) and y_column_names[i] else f"Y-Column {y_idx+1}"
    ax = axs[i] 

    print(f"\n--- Plotting graph for: {current_y_col_name} (original index {y_idx}) ---")

    print(f"Processing File 1 (With Coulomb) for Y-column {y_idx+1}: {file_path_str_1}")
    x1_values, y1_values = load_and_prepare_data(file_path_str_1, x_col_index, y_idx, "With Coulomb")

    print(f"Processing File 2 (No Coulomb) for Y-column {y_idx+1}: {file_path_str_2}")
    x2_values, y2_values = load_and_prepare_data(file_path_str_2, x_col_index, y_idx, "No Coulomb")

    plot_successful_for_this_subplot = False
    if x1_values is not None and y1_values is not None:
        ax.plot(x1_values, y1_values, linestyle='-',
                label=f"With Coulomb (File 1)", linewidth=1.5, color='blue')
        plot_successful_for_this_subplot = True
        at_least_one_plot_successful = True

    if x2_values is not None and y2_values is not None:
        ax.plot(x2_values, y2_values, linestyle='-',
                label=f"Without Coulomb (File 2)", linewidth=1.5, color='orange')
        plot_successful_for_this_subplot = True
        at_least_one_plot_successful = True

    if plot_successful_for_this_subplot:
        ax.set_ylabel(f"Value ({current_y_col_name})")
        ax.legend(loc='best')
        ax.grid(True)
    else:
        ax.text(0.5, 0.5, f"Failed to load data\n for Y-column {y_idx+1}",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, color='red')
        ax.grid(True) 


axs[-1].set_xlabel(f"X-axis (Column {x_col_index + 1})")


if at_least_one_plot_successful:
    plt.tight_layout(rect=[0, 0.03, 1, 0.96]) 
    plt.show()
    print("\nPlot generation complete. All plots are displayed in a single window.")
else:
    plt.close(fig) 
    print("\nFailed to load data for any of the plots.")