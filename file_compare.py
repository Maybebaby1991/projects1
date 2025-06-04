import difflib
import os

def compare_text_files(file_path1, file_path2):
    """
    Compares two text files and outputs the differences.

    Args:
        file_path1 (str): Path to the first file.
        file_path2 (str): Path to the second file.
    """
    print(f"Comparing files:\n  File 1: {file_path1}\n  File 2: {file_path2}\n")

    # 1. Check if files exist
    if not os.path.exists(file_path1):
        print(f"Error: File not found at path: {file_path1}")
        return
    if not os.path.exists(file_path2):
        print(f"Error: File not found at path: {file_path2}")
        return

    try:
        # 2. Read the content of the files
        with open(file_path1, 'r', encoding='utf-8') as f1:
            lines1 = f1.readlines()
        with open(file_path2, 'r', encoding='utf-8') as f2:
            lines2 = f2.readlines()

    except Exception as e:
        print(f"Error reading files: {e}") # Corrected this print statement for clarity
        return

    # 3. Compare the content
    if lines1 == lines2:
        print("Files are identical.")
    else:
        print("Files are different. The following differences were found:")
        print("--------------------------------------------------")

        diff = difflib.unified_diff(
            lines1,
            lines2,
            fromfile=os.path.basename(file_path1) + " (original)",
            tofile=os.path.basename(file_path2) + " (comparison)",
            lineterm=''
        )

        for line in diff:
            print(line.rstrip('\n'))
        print("--------------------------------------------------")
        print("End of differences.")

if __name__ == "__main__":
    # --- SET FILE PATHS HERE ---
    # Filename to compare
    file_name = "2p_Abs_at_zero.txt"  # Replace with your filename

    # Path to the first directory
    # Example for Windows: dir_path1 = r"C:\Users\YourUser\Documents\ProjectA"
    # Example for Linux/macOS: dir_path1 = "/home/user/project_alpha"
    dir_path1 = "D:/working harder making better/27_03_hBN_Coulomb/ConstCheckUncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-15EPS-1.0"  # Replace with your path

    # Path to the second directory
    # Example for Windows: dir_path2 = r"C:\Users\YourUser\Documents\ProjectB"
    # Example for Linux/macOS: dir_path2 = "/home/user/project_beta"
    dir_path2 = "D:/working harder making better/27_03_hBN_Coulomb/ConstCheckUncellArea__Nk_200intens_0.00e+00_t1_-2.3_Ncut20_qTF_0.01_dt_0.1_delayXUV_0w_Pump_R0-5EPS-1.0" # Replace with your path
    # ------------------------------------

    # Construct full file paths
    full_path1 = os.path.join(dir_path1, file_name)
    full_path2 = os.path.join(dir_path2, file_name)

    print(f"Starting comparison for file '{file_name}' in directories:")
    print(f"Directory 1: {dir_path1}")
    print(f"Directory 2: {dir_path2}")
    print("-" * 30)

    # Start the comparison
    compare_text_files(full_path1, full_path2)

    # --- Examples for a quick test (you can uncomment and adjust the paths above) ---
    # # Create test files for example
    # # Make sure the directories test_dir1_hardcoded and test_dir2_hardcoded exist
    # # or create them before running the test.
    # # For example, you can create them manually or add:
    # # os.makedirs("test_dir1_hardcoded", exist_ok=True)
    # # os.makedirs("test_dir2_hardcoded", exist_ok=True)

    # # Configure paths for test files
    # test_file_name = "sample_hardcoded.txt"
    # test_dir1 = "test_dir1_hardcoded"
    # test_dir2 = "test_dir2_hardcoded"

    # # # Create directories if they don't exist
    # os.makedirs(test_dir1, exist_ok=True)
    # os.makedirs(test_dir2, exist_ok=True)


    # # Example 1: Identical files
    # path_test1_file1 = os.path.join(test_dir1, test_file_name)
    # path_test1_file2 = os.path.join(test_dir2, test_file_name)
    # with open(path_test1_file1, "w", encoding="utf-8") as f:
    #     f.write("This is the first line.\n")
    #     f.write("This is the second line.\n")
    # with open(path_test1_file2, "w", encoding="utf-8") as f:
    #     f.write("This is the first line.\n")
    #     f.write("This is the second line.\n")
    # print("\n--- Test 1: Identical files (hardcoded paths) ---")
    # # Pass paths to compare_text_files explicitly
    # # compare_text_files(path_test1_file1, path_test1_file2)


    # # Example 2: Different files
    # diff_test_file_name = "diff_sample_hardcoded.txt"
    # path_test2_file1 = os.path.join(test_dir1, diff_test_file_name)
    # path_test2_file2 = os.path.join(test_dir2, diff_test_file_name)
    # with open(path_test2_file1, "w", encoding="utf-8") as f:
    #     f.write("Hello, world!\n")
    #     f.write("This is an old line.\n")
    #     f.write("A common line.\n")
    # with open(path_test2_file2, "w", encoding="utf-8") as f:
    #     f.write("Hello, world!\n")
    #     f.write("This is a new line.\n")
    #     f.write("A common line.\n")
    #     f.write("An additional line at the end.\n")
    # print("\n--- Test 2: Different files (hardcoded paths) ---")
    # # compare_text_files(path_test2_file1, path_test2_file2)