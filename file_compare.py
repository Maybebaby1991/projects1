import difflib
import os

def compare_text_files(file_path1, file_path2):
    """
    Сравнивает два текстовых файла и выводит различия.

    Args:
        file_path1 (str): Путь к первому файлу.
        file_path2 (str): Путь ко второму файлу.
    """
    print(f"Сравнение файлов:\n  Файл 1: {file_path1}\n  Файл 2: {file_path2}\n")

    # 1. Проверка существования файлов
    if not os.path.exists(file_path1):
        print(f"Ошибка: Файл не найден по пути: {file_path1}")
        return
    if not os.path.exists(file_path2):
        print(f"Ошибка: Файл не найден по пути: {file_path2}")
        return

    try:
        # 2. Чтение содержимого файлов
        with open(file_path1, 'r', encoding='utf-8') as f1:
            lines1 = f1.readlines()
        with open(file_path2, 'r', encoding='utf-8') as f2:
            lines2 = f2.readlines()

    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")
        return

    # 3. Сравнение содержимого
    if lines1 == lines2:
        print("Файлы идентичны.")
    else:
        print("Файлы различаются. Найдены следующие различия:")
        print("--------------------------------------------------")

        diff = difflib.unified_diff(
            lines1,
            lines2,
            fromfile=os.path.basename(file_path1) + " (оригинал)",
            tofile=os.path.basename(file_path2) + " (сравнение)",
            lineterm=''
        )

        for line in diff:
            print(line.rstrip('\n'))
        print("--------------------------------------------------")
        print("Конец различий.")

if __name__ == "__main__":
    # --- ЗАДАЙТЕ ЗДЕСЬ ПУТИ К ФАЙЛАМ ---
    # Имя файла, который нужно сравнить
    file_name = "2p_Abs_at_zero.txt"  # Замените на ваше имя файла

    # Путь к первой директории
    # Пример для Windows: dir_path1 = r"C:\Users\YourUser\Documents\ProjectA"
    # Пример для Linux/macOS: dir_path1 = "/home/user/project_alpha"
    dir_path1 = "D:/working harder making better/27_03_hBN_Coulomb/ConstCheckUncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0"  # Замените на ваш путь

    # Путь ко второй директории
    # Пример для Windows: dir_path2 = r"C:\Users\YourUser\Documents\ProjectB"
    # Пример для Linux/macOS: dir_path2 = "/home/user/project_beta"
    dir_path2 = "D:/working harder making better/27_03_hBN_Coulomb/ConstCheckUncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0" # Замените на ваш путь
    # ------------------------------------

    # Формируем полные пути к файлам
    full_path1 = os.path.join(dir_path1, file_name)
    full_path2 = os.path.join(dir_path2, file_name)

    print(f"Запускаю сравнение для файла '{file_name}' в директориях:")
    print(f"Директория 1: {dir_path1}")
    print(f"Директория 2: {dir_path2}")
    print("-" * 30)

    # Запускаем сравнение
    compare_text_files(full_path1, full_path2)

    # --- Примеры для быстрого теста (можно раскомментировать и настроить пути выше) ---
    # # Создадим тестовые файлы для примера
    # # Убедитесь, что директории test_dir1_hardcoded и test_dir2_hardcoded существуют
    # # или создайте их перед запуском теста.
    # # Например, можно создать их вручную или добавить:
    # # os.makedirs("test_dir1_hardcoded", exist_ok=True)
    # # os.makedirs("test_dir2_hardcoded", exist_ok=True)

    # # Настройте пути для тестовых файлов
    # test_file_name = "sample_hardcoded.txt"
    # test_dir1 = "test_dir1_hardcoded"
    # test_dir2 = "test_dir2_hardcoded"

    # # # Создаем директории, если их нет
    # os.makedirs(test_dir1, exist_ok=True)
    # os.makedirs(test_dir2, exist_ok=True)


    # # Пример 1: Идентичные файлы
    # path_test1_file1 = os.path.join(test_dir1, test_file_name)
    # path_test1_file2 = os.path.join(test_dir2, test_file_name)
    # with open(path_test1_file1, "w", encoding="utf-8") as f:
    #     f.write("Это первая строка.\n")
    #     f.write("Это вторая строка.\n")
    # with open(path_test1_file2, "w", encoding="utf-8") as f:
    #     f.write("Это первая строка.\n")
    #     f.write("Это вторая строка.\n")
    # print("\n--- Тест 1: Идентичные файлы (жестко заданные пути) ---")
    # # Передаем пути к compare_text_files явно
    # # compare_text_files(path_test1_file1, path_test1_file2)


    # # Пример 2: Различные файлы
    # diff_test_file_name = "diff_sample_hardcoded.txt"
    # path_test2_file1 = os.path.join(test_dir1, diff_test_file_name)
    # path_test2_file2 = os.path.join(test_dir2, diff_test_file_name)
    # with open(path_test2_file1, "w", encoding="utf-8") as f:
    #     f.write("Привет, мир!\n")
    #     f.write("Это старая строка.\n")
    #     f.write("Общая строка.\n")
    # with open(path_test2_file2, "w", encoding="utf-8") as f:
    #     f.write("Привет, мир!\n")
    #     f.write("Это новая строка.\n")
    #     f.write("Общая строка.\n")
    #     f.write("Дополнительная строка в конце.\n")
    # print("\n--- Тест 2: Различные файлы (жестко заданные пути) ---")
    # # compare_text_files(path_test2_file1, path_test2_file2)