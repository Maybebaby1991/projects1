import os
import re
import numpy as np
import matplotlib.pyplot as plt

BASE_PATH = r"D:\working harder making better\27_03_hBN_Coulomb"


folder_names_to_process = [
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-30EPS-1.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.2",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.5",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-2.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0"
    # Add other full folder names here if needed, except for NOCOULOMB
]

# Name of the NOCOULOMB folder
nocoulomb_folder_name = "NOCOULOMB_Nk_200intens_0.00e+00_t1_-2.3_dt_0.1"


file_x_name = "2p_w_at_zero.txt"
file_y_name = "2p_Abs_at_zero.txt"

# Parameters for filtering when plotting graphs
TARGET_EPS_FOR_R0_PLOT = 1.0  # At what EPS value do we plot the dependency on R0
TARGET_R0_FOR_EPS_PLOT = 10.0 # At what R0 value do we plot the dependency on EPS


def extract_params_from_folder_name(folder_name):
    """Extracts R0 and EPS from the folder name."""
    match_r0_eps = re.search(r"R0-(\d+\.?\d*)EPS-(\d+\.?\d*)", folder_name)
    if match_r0_eps:
        r0 = float(match_r0_eps.group(1))
        eps = float(match_r0_eps.group(2))
        return r0, eps
    # Fallback if R0 and EPS are not together or one is missing
    match_r0 = re.search(r"R0-(\d+\.?\d*)", folder_name)
    r0 = float(match_r0.group(1)) if match_r0 else None

    match_eps = re.search(r"EPS-(\d+\.?\d*)", folder_name)
    eps = float(match_eps.group(1)) if match_eps else None

    return r0, eps


def read_data_from_folder(folder_path, x_file, y_file):
    """Reads X and Y data from the specified files in the folder."""
    try:
        path_x = os.path.join(folder_path, x_file)
        path_y = os.path.join(folder_path, y_file)

        data_x = np.loadtxt(path_x)
        data_y = np.loadtxt(path_y)

        return data_x, data_y
    except FileNotFoundError:
        print(f"Error: One of the files ({x_file}, {y_file}) not found in folder {folder_path}")
        return None, None
    except Exception as e:
        print(f"Error reading data from {folder_path}: {e}")
        return None, None

all_data = []

# Process NOCOULOMB data first
nocoulomb_full_path = os.path.join(BASE_PATH, nocoulomb_folder_name)
print(f"Processing NOCOULOMB: {nocoulomb_full_path}")
nc_x, nc_y = read_data_from_folder(nocoulomb_full_path, file_x_name, file_y_name)
if nc_x is None or nc_y is None:
    print(f"Failed to read NOCOULOMB data. The script cannot continue without this data.")
    exit()

for folder_name in folder_names_to_process:
    full_folder_path = os.path.join(BASE_PATH, folder_name)
    print(f"Processing: {folder_name}")

    r0, eps = extract_params_from_folder_name(folder_name)
    if r0 is None or eps is None:
        print(f"  -> Could not extract R0 and/or EPS from folder name: {folder_name}. Skipping.")
        continue

    data_x, data_y = read_data_from_folder(full_folder_path, file_x_name, file_y_name)
    if data_x is not None and data_y is not None:
        all_data.append({
            "name": folder_name,
            "r0": r0,
            "eps": eps,
            "x": data_x,
            "y": data_y
        })


plt.figure(figsize=(10, 7))
plt.title(f"Dependency on R0 (for EPS = {TARGET_EPS_FOR_R0_PLOT})")
plt.xlabel("2p_w_at_zero (X-axis)")
plt.ylabel("2p_Abs_at_zero (Y-axis)")


plt.plot(nc_x, nc_y, label="NOCOULOMB", linestyle="--", color="black")


plot_data_r0 = sorted([d for d in all_data if d["eps"] == TARGET_EPS_FOR_R0_PLOT], key=lambda item: item["r0"])

if not plot_data_r0:
    print(f"No data found to plot for R0 dependency with EPS={TARGET_EPS_FOR_R0_PLOT}")
else:
    for data_item in plot_data_r0:
        plt.plot(data_item["x"], data_item["y"], label=f"R0={data_item['r0']:.1f}, EPS={data_item['eps']:.1f}")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.figure(figsize=(10, 7))
plt.title(f"Dependency on EPS (for R0 = {TARGET_R0_FOR_EPS_PLOT})")
plt.xlabel("2p_w_at_zero (X-axis)")
plt.ylabel("2p_Abs_at_zero (Y-axis)")

plt.plot(nc_x, nc_y, label="NOCOULOMB", linestyle="--", color="black")

# Filter and sort data for the EPS plot
plot_data_eps = sorted([d for d in all_data if d["r0"] == TARGET_R0_FOR_EPS_PLOT], key=lambda item: item["eps"])

if not plot_data_eps:
     print(f"No data found to plot for EPS dependency with R0={TARGET_R0_FOR_EPS_PLOT}")
else:
    for data_item in plot_data_eps:
        plt.plot(data_item["x"], data_item["y"], label=f"R0={data_item['r0']:.1f}, EPS={data_item['eps']:.1f}")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()

print("Plotting complete.")