import zipfile
import os
import argparse 
import re
import pathlib

def read_file_from_zip(zip_path, file_name):
    """
    Reads a file from a .zip archive without extracting it.

    Args:
        zip_path (str): Path to the .zip archive.
        file_name (str): Name of the file inside the .zip archive to read.

    Returns:
        str: Contents of the file, or None if the file does not exist.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as file:
                    content = file.read().decode('utf-8')
                    return content
            else:
                print(f"File '{file_name}' not found in the archive.")
                return None
    except zipfile.BadZipFile:
        print(f"Error: The file '{zip_path}' is not a valid zip file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_dataset_info_from_archive(zip_path, file_name):

    def extract_info(text):
        """
        Extracts URL and license information from the provided text.

        Args:
            text (str): Text containing the URL and license.

        Returns:
            tuple: A tuple containing the URL and the license extracted from the text.
        """
        # Regex pattern to find URL (simplified version)
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, text)

        # Regex pattern to find license
        license_pattern = r'License: (.+)$'
        license_match = re.search(license_pattern, text, re.MULTILINE)

        # Extract URL and license if found
        url = url_match.group(0) if url_match else None
        license_info = license_match.group(1) if license_match else None

        return url, license_info


    content = read_file_from_zip(zip_path, file_name)
    return extract_info(content)

# Example usage
file_name = 'README.dataset.txt'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read a specific file from a ZIP archive without extracting the entire archive.")
    parser.add_argument("path", help="The path to the .zip file from which to read.")

    args = parser.parse_args()
    path = pathlib.Path(args.path).expanduser().resolve()
    if path.is_dir():
        paths = [pathlib.Path(x) for x in path.iterdir()]
        paths = [x for x in paths if x.suffix == ".zip"]
        if len(paths) == 0:
            raise ValueError(f"No .zip archives were found at path: {str(path)}")
        for path in paths:
            info = get_dataset_info_from_archive(path, file_name)
            print(f"Dataset file: {path.name:<40} license: {info[1]:<20} url: {info[0]}")
    elif path.suffix == ".zip":
        info = get_dataset_info_from_archive(path, file_name)
    else:
        raise ValueError(f"Path {str(path)} provided is not a .zip archive or a directory")

# python ./scripts/read_license.py ~/.dataset/chess-vision/external_dataset