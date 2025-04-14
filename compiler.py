import os
import zipfile

RESOURCES_PATH = "resources"
COMPILED_PATH = "compiled"
COMPILED_ZIP_PATH = COMPILED_PATH + "/compiled.zip"

def resources_exists() -> bool:
    """
    Check if the resources directory exists.
    """
    return os.path.exists(RESOURCES_PATH)

def resources_filled() -> [list[str], list[str]]:
    """
    Check if the resources directory is filled with .zip files
    """
    list_dir = os.listdir(RESOURCES_PATH)
    zip_files_list = [f for f in list_dir if f.endswith('.zip')]
    non_zip_files_list = [f for f in list_dir if not f.endswith('.zip')]
    return [zip_files_list, non_zip_files_list]

def sorting_filtering_files_of_correct_format(files: list[str]) -> [list[str], list[str]]:
    """
    List the files of a correct format
    """
    filtered_files = []
    invalid_files = []

    for f in files:
        if not ("_" in f and f.split("_")[0].isnumeric()):
            invalid_files.append(f)
        else:
            filtered_files.append(f)

    valid_files = [f for f in sorted(filtered_files, key=lambda x: int(x.split("_")[0]))]

    return [valid_files, invalid_files]

def compiled_exists() -> bool:
    """
    Check if the compiled directory exists.
    """
    return os.path.exists(COMPILED_PATH)

def create_compiled_dir() -> None:
    """
    Create the compiled directory
    """
    os.makedirs(COMPILED_PATH)

def compiled_zip_already_exists() -> bool:
    """
    Check if the compiled zip file already exists.
    """
    return os.path.exists(COMPILED_ZIP_PATH)

def compiled_empty() -> bool:
    """
    Check if the compiled directory is empty.
    """
    return len(os.listdir(COMPILED_PATH)) == 0

def unzip_file_into_compiled(file_path: str) -> None:
    """
    Unzip a file in the compiled directory.
    """
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(COMPILED_PATH)

def create_compiled_zip() -> None:
    """
    Create the compiled zip file.
    """
    with zipfile.ZipFile(COMPILED_ZIP_PATH, 'w') as zip_ref:
        for folder, subfolders, filenames in os.walk(COMPILED_PATH):
            for filename in filenames:
                if filename != "compiled.zip":
                    file_path = os.path.join(folder, filename)
                    zip_ref.write(file_path, os.path.relpath(file_path, COMPILED_PATH))

def clean_compiled_dir() -> None:
    """
    Clean the compiled directory except the compiled.zip file.
    """
    for folder, subfolders, filenames in os.walk(COMPILED_PATH):
        for filename in filenames:
            if filename != "compiled.zip":
                file_path = os.path.join(folder, filename)
                os.remove(file_path)
        for subfolder in subfolders:
            folder_path = os.path.join(folder, subfolder)
            os.rmdir(folder_path)

if __name__ == "__main__":
    # Tell the user that the compilation is starting
    print("Compiling...")

    # Check if the resources directory exists
    if not resources_exists():
        print("Resources directory does not exist. Please ensure that all necessary files are in place. Read the README.md file for more information.")
        exit(1)
    print("Resources directory detected...")

    # Listing the files in the resources directory
    print("Listing files in the resources directory...")
    [zip_files, non_zip_files] = resources_filled()

    # Check if the resources directory has with .zip files
    if not zip_files:
        print("No .zip files found in the resources directory. Please ensure that all necessary files are in place. Read the README.md file for more information.")
        exit(2)

    # Counting the number of .zip files
    print(f"Found {len(zip_files)} .zip files in the resources directory...")

    # Listing the ignored files for the user
    if non_zip_files:
        print("The following files were ignored because they are not .zip files :")
        for file in non_zip_files:
            print(f" - {file}")
    else:
        print("No files were ignored...")

    # Listing the files of a correct format
    print("Listing the zip files matching the correct format...")
    [valid_zip_files, zip_invalid_files] = sorting_filtering_files_of_correct_format(zip_files)

    # Check if there are valid files
    if not valid_zip_files:
        print("No valid files found. Please ensure that all necessary files are in place. Read the README.md file for more information.")
        exit(3)

    # Counting the number of valid files
    print(f"Found {len(valid_zip_files)} valid zip files in the resources directory...")

    # Listing the invalid files for the user
    if zip_invalid_files:
        print("The following files were ignored because they are not valid format zip files :")
        for file in zip_invalid_files:
            print(f" - {file}")
    else:
        print("No invalid files found...")

    # Creating the compiled directory if it does not exist
    if not compiled_exists():
        print("Creating the compiled directory...")
        create_compiled_dir()
    else:
        print("Compiled directory already exists...")

    # Check if the compiled file already exists
    if compiled_zip_already_exists():
        print(f"The compiled.zip file already exists in the {COMPILED_PATH} directory. Please delete it before compiling again. (Secure mode)")
        exit(4)

    # Tell the user that the compilation is starting
    print("Compilation stage starting...")

    # Unzipping the files in the compiled directory
    print("Unzipping the files in the compiled directory in order...")
    for file in reversed(valid_zip_files):
        print(f"Unzipping {file}...")
        unzip_file_into_compiled(os.path.join(RESOURCES_PATH, file))

    # Check if there was something in the zipped files
    if compiled_empty():
        print("The compiled directory is empty. Please ensure that all necessary files are in place. Read the README.md file for more information.")
        exit(5)

    # Check if there was a compiled.zip in the zipped files
    if compiled_zip_already_exists():
        print("The compiled.zip file was found in the zipped files. Please delete it before compiling again. (Secure mode)")
        exit(6)

    # Creating the compiled zip file
    print("Creating the compiled zip file...")
    create_compiled_zip()

    # Check if the compiled zip file was created
    if not compiled_zip_already_exists():
        print("The compiled.zip file was not created. Please ensure that all necessary files are in place. Read the README.md file for more information.")
        exit(7)

    # Cleaning the compiled directory
    print("Cleaning the compiled directory except compiled.zip...")
    clean_compiled_dir()

    print("Compilation finished successfully.")
    exit(0)
