import matplotlib.pyplot as plt
import pandas as pd
import os
file_path_str = r"\D:\working harder making better\27_03_hBN_Coulomb\ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0\ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0_6.00\Output\Losses.txt"
if not os.path.exists(file_path_str):
print(f"Error: The file was not found on the path: {file_path_str}")
else:
try:
data = pd.read_csv(file_path_str, delim_whitespace=True, header=None, comment='#')
if data.shape[1] < 4:
        print(f"Error {file_path_str} there are less than 4 columns in the file")
    else:
        # Извлекаем данные
        x_values = data.iloc[:, 0]  
        y_columns_data = [
            data.iloc[:, 1],  
            data.iloc[:, 2],  
            data.iloc[:, 3]   
        ]
        
        y_column_names = [
            "Second Column",
            "Third Column",
            "Fourth Column" 
        ]
        fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True) 
        fig.suptitle("Losses", fontsize=16)
        for i in range(3):
            axs[i].plot(x_values, y_columns_data[i], marker='.', linestyle='-', label=y_column_names[i],linewidth=0.5,markersize=2) 
            axs[i].set_ylabel(f"{y_column_names[i]}")
            axs[i].set_title(f"Graph {y_column_names[i]}") 
            axs[i].legend(loc='best') 
            axs[i].grid(True)          
        axs[2].set_xlabel("Time")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])           
        plt.show()       
        print("All plots are displayed in a single window.")
except pd.errors.EmptyDataError:
    print(f"Error: File {file_path_str} empty.")
except Exception as e:
    print(f"An error occurred while reading or processing the file: {e}")