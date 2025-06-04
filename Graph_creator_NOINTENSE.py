import os
import re
import numpy as np
import matplotlib.pyplot as plt

BASE_PATH = r"D:\working harder making better\27_03_hBN_Coulomb"

folder_names_to_process = [
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0",
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-30EPS-1.0",
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0",
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.2",
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.5",
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-2.0",
    "ReCalc_UncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0"
]

nocoulomb_folder_name = "NOCOULOMB_Nk_200intens_0.00e+00_t1_-2.3_dt_0.1"

file_x_name_default = "2p_w_at_zero.txt"
file_y_name_default = "2p_Abs_at_zero.txt"

file_x_name_nocoulomb = "2p_w_no_pump.txt"
file_y_name_nocoulomb = "2p_Abs_no_pump.txt"

FIXED_R0_FOR_EPS_PLOT = 10.0
FIXED_EPS_FOR_R0_PLOT = 1.0
FLOAT_COMPARISON_TOLERANCE = 1e-6

def extract_params_from_folder_name(folder_name):
    match_r0_eps = re.search(r"R0-(\d+\.?\d*)EPS-(\d+\.?\d*)", folder_name)
    if match_r0_eps:
        try:
            r0 = float(match_r0_eps.group(1))
            eps = float(match_r0_eps.group(2))
            return r0, eps
        except ValueError:
            print(f"  Warning: Could not convert R0/EPS to numbers for folder: {folder_name}")
            return None, None
    r0_val, eps_val = None, None
    match_r0 = re.search(r"R0-(\d+\.?\d*)", folder_name)
    if match_r0:
        try:
            r0_val = float(match_r0.group(1))
        except ValueError:
            print(f"  Warning: Could not convert R0 to number for folder: {folder_name}")
    match_eps = re.search(r"EPS-(\d+\.?\d*)", folder_name)
    if match_eps:
        try:
            eps_val = float(match_eps.group(1))
        except ValueError:
            print(f"  Warning: Could not convert EPS to number for folder: {folder_name}")
    if r0_val is not None and eps_val is not None:
        return r0_val, eps_val
    return None, None

def read_data_from_folder(folder_path, x_file, y_file):
    try:
        path_x = os.path.join(folder_path, x_file)
        path_y = os.path.join(folder_path, y_file)
        
        if not os.path.exists(path_x):
            print(f"Error: File X ({path_x}) not found.")
            return None, None
        if not os.path.exists(path_y):
            print(f"Error: File Y ({path_y}) not found.")
            return None, None
            
        data_x = np.loadtxt(path_x)
        data_y = np.loadtxt(path_y)
        return data_x, data_y
    except Exception as e:
        print(f"Error reading data from {folder_path} (files {x_file}, {y_file}): {e}")
        return None, None

all_processed_data = []

nocoulomb_full_path = os.path.join(BASE_PATH, nocoulomb_folder_name)
print(f"Processing NOCOULOMB: {nocoulomb_full_path}")
print(f"  Using files: {file_x_name_nocoulomb}, {file_y_name_nocoulomb}")
nc_x, nc_y = read_data_from_folder(nocoulomb_full_path, file_x_name_nocoulomb, file_y_name_nocoulomb)
if nc_x is None or nc_y is None:
    print(f"CRITICAL ERROR: Failed to read NOCOULOMB data. Exiting.")
    exit()

print("\n--- Processing parameterized folders ---")
for folder_name in folder_names_to_process:
    full_folder_path = os.path.join(BASE_PATH, folder_name)
    print(f"Attempting to process folder: {folder_name}")
    if not os.path.isdir(full_folder_path):
        print(f"  WARNING: Folder not found at path: {full_folder_path}. Skipping.")
        continue
        
    r0, eps = extract_params_from_folder_name(folder_name)
    if r0 is None or eps is None:
        print(f"  -> Failed to extract valid R0 and EPS from folder name: {folder_name}. Skipping.")
        continue
    print(f"  Extracted: R0={r0}, EPS={eps}")
    
    print(f"  Using files: {file_x_name_default}, {file_y_name_default}")
    data_x, data_y = read_data_from_folder(full_folder_path, file_x_name_default, file_y_name_default)
    if data_x is not None and data_y is not None:
        all_processed_data.append({
            "name": folder_name,
            "r0": r0,
            "eps": eps,
            "x": data_x,
            "y": data_y
        })
        print(f"  Data for {folder_name} loaded successfully.")
    else:
        print(f"  Failed to load data for {folder_name}.")

print("\n--- Debug information: All loaded data (all_processed_data) ---")
if not all_processed_data:
    print("List all_processed_data is empty! Check folder names and paths.")
else:
    for item in all_processed_data:
        print(f"  Folder: {item['name']}, R0: {item['r0']}, EPS: {item['eps']}, X_shape: {item['x'].shape}, Y_shape: {item['y'].shape}")
print("--- End of debug information ---\n")


fig, axs = plt.subplots(2, 1, figsize=(12, 14), sharex=True)

ax_eps = axs[0]
ax_eps.set_title(f"Dependency on EPS (at R0 ≈ {FIXED_R0_FOR_EPS_PLOT})")
ax_eps.set_ylabel(f"{file_y_name_default} (Y-axis)")

ax_eps.plot(nc_x, nc_y, label="NOCOULOMB (no_pump)", linestyle="--", color="black", linewidth=1.5)

plot_data_for_eps_plot = sorted(
    [d for d in all_processed_data if abs(d["r0"] - FIXED_R0_FOR_EPS_PLOT) < FLOAT_COMPARISON_TOLERANCE],
    key=lambda item: item["eps"]
)

print(f"Data for 'Dependency on EPS' plot (R0 ≈ {FIXED_R0_FOR_EPS_PLOT}):")
if not plot_data_for_eps_plot:
    print("  No suitable data found!")
else:
    for item in plot_data_for_eps_plot:
        print(f"  Plotting data for: R0={item['r0']}, EPS={item['eps']}")
        ax_eps.plot(item["x"], item["y"], label=f"EPS={item['eps']:.1f} (R0={item['r0']:.1f})")
ax_eps.legend()
ax_eps.grid(True)
# Set x-axis limit for the top plot (optional if sharex works as expected for initial limits, but safer)
# ax_eps.set_xlim(left=-3)


ax_r0 = axs[1]
ax_r0.set_title(f"Dependency on R0 (at EPS ≈ {FIXED_EPS_FOR_R0_PLOT})")
ax_r0.set_xlabel(f"{file_x_name_default} (X-axis)")
ax_r0.set_ylabel(f"{file_y_name_default} (Y-axis)")

ax_r0.plot(nc_x, nc_y, label="NOCOULOMB (no_pump)", linestyle="--", color="black", linewidth=1.5)

plot_data_for_r0_plot = sorted(
    [d for d in all_processed_data if abs(d["eps"] - FIXED_EPS_FOR_R0_PLOT) < FLOAT_COMPARISON_TOLERANCE],
    key=lambda item: item["r0"]
)

print(f"\nData for 'Dependency on R0' plot (EPS ≈ {FIXED_EPS_FOR_R0_PLOT}):")
if not plot_data_for_r0_plot:
    print("  No suitable data found!")
else:
    for item in plot_data_for_r0_plot:
        print(f"  Plotting data for: R0={item['r0']}, EPS={item['eps']}")
        ax_r0.plot(item["x"], item["y"], label=f"R0={item['r0']:.1f} (EPS={item['eps']:.1f})")
ax_r0.legend()
ax_r0.grid(True)

# Set x-axis limit to start from -3 for the bottom plot
# Since sharex=True, this should also apply to the top plot.
ax_r0.set_xlim(left=-3)


plt.tight_layout(pad=2.5)
fig.suptitle("Absorption Spectra Comparison", fontsize=16, y=1.01)
plt.show()

print("\nPlotting complete.")