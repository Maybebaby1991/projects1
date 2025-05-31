import os
import re
import numpy as np
import matplotlib.pyplot as plt

# --- КОНФИГУРАЦИЯ ---
BASE_PATH = r"D:\working harder making better\27_03_hBN_Coulomb" # Используйте r"..." для путей Windows

# Список названий папок для обработки (вручную)
folder_names_to_process = [
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-30EPS-1.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.2",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-1.5",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-10EPS-2.0",
    "ReCalc_UncellArea_..._Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0"
    # Добавьте сюда остальные полные имена папок, если нужно, кроме NOCOULOMB
]

# Название папки NOCOULOMB
nocoulomb_folder_name = "NOCOULOMB_Nk_200intens_0.00e+00_t1_-2.3_dt_0.1" # Уточните полное имя, если оно другое

# Имена файлов данных
file_x_name = "2p_w_at_zero.txt"
file_y_name = "2p_Abs_at_zero.txt"

# Параметры для фильтрации при построении графиков
TARGET_EPS_FOR_R0_PLOT = 1.0  # При каком значении EPS строим график зависимости от R0
TARGET_R0_FOR_EPS_PLOT = 10.0 # При каком значении R0 строим график зависимости от EPS
# --- КОНЕЦ КОНФИГУРАЦИИ ---

def extract_params_from_folder_name(folder_name):
    """Извлекает R0 и EPS из имени папки."""
    match_r0_eps = re.search(r"R0-(\d+\.?\d*)EPS-(\d+\.?\d*)", folder_name)
    if match_r0_eps:
        r0 = float(match_r0_eps.group(1))
        eps = float(match_r0_eps.group(2))
        return r0, eps
    
    # Если стандартный паттерн не найден, попробуем найти только R0 или только EPS
    # (хотя по вашим примерам они всегда вместе, кроме NOCOULOMB)
    match_r0 = re.search(r"R0-(\d+\.?\d*)", folder_name)
    r0 = float(match_r0.group(1)) if match_r0 else None
    
    match_eps = re.search(r"EPS-(\d+\.?\d*)", folder_name)
    eps = float(match_eps.group(1)) if match_eps else None
    
    return r0, eps


def read_data_from_folder(folder_path, x_file, y_file):
    """Читает данные X и Y из указанных файлов в папке."""
    try:
        path_x = os.path.join(folder_path, x_file)
        path_y = os.path.join(folder_path, y_file)
        
        data_x = np.loadtxt(path_x)
        data_y = np.loadtxt(path_y)
        
        return data_x, data_y
    except FileNotFoundError:
        print(f"Ошибка: Один из файлов ({x_file}, {y_file}) не найден в папке {folder_path}")
        return None, None
    except Exception as e:
        print(f"Ошибка при чтении данных из {folder_path}: {e}")
        return None, None

# --- Основная логика ---
all_data = []

# 1. Чтение данных из папки NOCOULOMB
nocoulomb_full_path = os.path.join(BASE_PATH, nocoulomb_folder_name)
print(f"Обработка NOCOULOMB: {nocoulomb_full_path}")
nc_x, nc_y = read_data_from_folder(nocoulomb_full_path, file_x_name, file_y_name)
if nc_x is None or nc_y is None:
    print(f"Не удалось прочитать данные NOCOULOMB. Скрипт не может продолжить без этих данных.")
    exit()

# 2. Чтение данных из остальных папок
for folder_name in folder_names_to_process:
    full_folder_path = os.path.join(BASE_PATH, folder_name)
    print(f"Обработка: {folder_name}")
    
    r0, eps = extract_params_from_folder_name(folder_name)
    if r0 is None or eps is None:
        print(f"  -> Не удалось извлечь R0 и EPS из имени папки: {folder_name}. Пропуск.")
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

# 3. Построение графика с различными R0 (EPS фиксирован)
plt.figure(figsize=(10, 7))
plt.title(f"Зависимость от R0 (при EPS = {TARGET_EPS_FOR_R0_PLOT})")
plt.xlabel("2p_w_at_zero (X-axis)")
plt.ylabel("2p_Abs_at_zero (Y-axis)")

# Сначала график NOCOULOMB
plt.plot(nc_x, nc_y, label="NOCOULOMB", linestyle="--", color="black")

# Данные для графика R0
plot_data_r0 = sorted([d for d in all_data if d["eps"] == TARGET_EPS_FOR_R0_PLOT], key=lambda item: item["r0"])

if not plot_data_r0:
    print(f"Не найдено данных для построения графика R0 при EPS={TARGET_EPS_FOR_R0_PLOT}")
else:
    for data_item in plot_data_r0:
        plt.plot(data_item["x"], data_item["y"], label=f"R0={data_item['r0']:.1f}, EPS={data_item['eps']:.1f}")

plt.legend()
plt.grid(True)
plt.tight_layout()

# 4. Построение графика с различными EPS (R0 фиксирован)
plt.figure(figsize=(10, 7))
plt.title(f"Зависимость от EPS (при R0 = {TARGET_R0_FOR_EPS_PLOT})")
plt.xlabel("2p_w_at_zero (X-axis)")
plt.ylabel("2p_Abs_at_zero (Y-axis)")

# Сначала график NOCOULOMB
plt.plot(nc_x, nc_y, label="NOCOULOMB", linestyle="--", color="black")

# Данные для графика EPS
plot_data_eps = sorted([d for d in all_data if d["r0"] == TARGET_R0_FOR_EPS_PLOT], key=lambda item: item["eps"])

if not plot_data_eps:
     print(f"Не найдено данных для построения графика EPS при R0={TARGET_R0_FOR_EPS_PLOT}")
else:
    for data_item in plot_data_eps:
        plt.plot(data_item["x"], data_item["y"], label=f"R0={data_item['r0']:.1f}, EPS={data_item['eps']:.1f}")

plt.legend()
plt.grid(True)
plt.tight_layout()

# Показать все графики
plt.show()

print("Построение графиков завершено.")