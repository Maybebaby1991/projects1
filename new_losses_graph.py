import matplotlib.pyplot as plt
import pandas as pd
import os

# Пути к файлам
file_path_str_1 = r"\\?\D:\working harder making better\27_03_hBN_Coulomb\ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0\ConstCheckUncellArea__Nk_200intens_1.00e+09_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0_6.00\Output\Losses.txt"
file_path_str_2 = r"D:\working harder making better\27_03_hBN_Coulomb\NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1\NOCOULOMB_Nk_200intens_1.00e+09_t1_-2.3_dt_0.1_6.00\Output\Losses.txt"

# Индекс колонки для X-оси (первая колонка)
x_col_index = 0

# Индексы колонок для Y-оси (вторая, третья, четвертая)
y_col_indices = [1, 2, 3] # Соответствует колонкам 2, 3, 4

# Названия для Y-колонок (для заголовков и меток)
y_column_names = [
    "",
    "",
    ""
]

def load_and_prepare_data(file_path, x_col_idx, y_col_idx, file_label=""):
    """
    Загружает данные из файла, проверяет и извлекает нужные колонки.
    Возвращает (x_values, y_values) или (None, None) в случае ошибки.
    """
    if not os.path.exists(file_path):
        print(f"Error: Файл не найден по пути ({file_label}, Y-кол: {y_col_idx+1}): {file_path}")
        return None, None
    
    try:
        data = pd.read_csv(file_path, delim_whitespace=True, header=None, comment='#')
        
        if data.empty:
            print(f"Error: Файл {file_path} ({file_label}, Y-кол: {y_col_idx+1}) пуст.")
            return None, None

        required_cols = max(x_col_idx, y_col_idx) + 1
        if data.shape[1] < required_cols:
            print(f"Error {file_path} ({file_label}, Y-кол: {y_col_idx+1}): В файле меньше {required_cols} колонок (найдено {data.shape[1]}). Необходимы колонки {x_col_idx+1} и {y_col_idx+1}.")
            return None, None
            
        x_values = data.iloc[:, x_col_idx]
        y_values = data.iloc[:, y_col_idx]
        return x_values, y_values
        
    except pd.errors.EmptyDataError:
        print(f"Error: Файл {file_path} ({file_label}, Y-кол: {y_col_idx+1}) пуст (pd.errors.EmptyDataError).")
        return None, None
    except Exception as e:
        print(f"Произошла ошибка при чтении или обработке файла {file_path} ({file_label}, Y-кол: {y_col_idx+1}): {e}")
        return None, None

# Создаем фигуру с 3 subplot'ами, расположенными вертикально
fig, axs = plt.subplots(len(y_col_indices), 1, figsize=(12, 15), sharex=True) 
fig.suptitle("Сравнение данных из файлов Losses", fontsize=18)

at_least_one_plot_successful = False

# Цикл по индексам Y-колонок
for i, y_idx in enumerate(y_col_indices):
    current_y_col_name = y_column_names[i]
    ax = axs[i] # Текущие оси для subplot'а

    print(f"\n--- Построение графика для Y: {current_y_col_name} (индекс {y_idx}) ---")

    # Загружаем данные из первого файла ("Coulomb" case)
    print(f"Обработка файла 1 (Coulomb) для Y-колонки {y_idx+1}: {file_path_str_1}")
    x1_values, y1_values = load_and_prepare_data(file_path_str_1, x_col_index, y_idx, "Coulomb")

    # Загружаем данные из второго файла ("No Coulomb" case)
    print(f"Обработка файла 2 (No Coulomb) для Y-колонки {y_idx+1}: {file_path_str_2}")
    x2_values, y2_values = load_and_prepare_data(file_path_str_2, x_col_index, y_idx, "No Coulomb")

    plot_successful_for_this_subplot = False
    # График для первого файла
    if x1_values is not None and y1_values is not None:
        ax.plot(x1_values, y1_values, linestyle='-', 
                label=f"С кулоном (File 1)", linewidth=1.5, color='blue') 
        plot_successful_for_this_subplot = True
        at_least_one_plot_successful = True
        
    # График для второго файла
    if x2_values is not None and y2_values is not None:
        ax.plot(x2_values, y2_values, linestyle='-', 
                label=f"Без кулона (File 2)", linewidth=1.5, color='orange') 
        plot_successful_for_this_subplot = True
        at_least_one_plot_successful = True

    if plot_successful_for_this_subplot:
        ax.set_ylabel(f"Значение ({current_y_col_name})") 
        ax.set_title(f"") 
        ax.legend(loc='best') 
        ax.grid(True)
    else:
        ax.text(0.5, 0.5, f"Не удалось загрузить данные\n для Y-колонки {y_idx+1}", 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=12, color='red')
        ax.grid(True) # Все равно показать сетку для единообразия

# Устанавливаем общую метку для оси X для нижнего графика
axs[-1].set_xlabel(f"Ось X (Колонка {x_col_index + 1})")

if at_least_one_plot_successful:
    plt.tight_layout(rect=[0, 0.03, 1, 0.96]) # Оставляем место для suptitle
    plt.show()       
    print("\nГрафики построены.")
else:
    plt.close(fig) # Закрыть пустую фигуру, если ничего не построено
    print("\nНе удалось загрузить данные ни для одного из графиков.")