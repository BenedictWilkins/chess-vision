import os
from PIL import Image
from tqdm import tqdm
import argparse
import pathlib
import shutil

supported_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}

def get_files_and_counts(source_dir):
    extension_count = {ext: 0 for ext in supported_extensions}
    extension_count['unrecognized'] = 0
    dirs = os.listdir(source_dir)
    result = []
    for filename in dirs:
        ext = pathlib.Path(filename).suffix
        if ext in supported_extensions:
            extension_count[ext] += 1
            result.append(filename)
        else:
            extension_count['unrecognized'] += 1
    return result, extension_count
    

def convert_images_to_png(source_dir, replace=False):
    """
    Converts all images in the specified directory to PNG format.
    
    Args:
    source_dir (str): Directory containing the images to be converted.
    """
    print(f"Reading files in {args.directory}...")
    output_dir = str(pathlib.Path(source_dir)) + "_png"
    if not replace:
        os.makedirs(output_dir, exist_ok=True)
    dirs = list(os.listdir(source_dir))
    dirs, counts = get_files_and_counts(source_dir)
    for ext, count in counts.items():
        print(f"Found {ext:<12} files: {count}")
    
    print(f"Converting {sum([counts[x] for x in supported_extensions])} files to '.png'...")
    for filename in tqdm(dirs):
        file_path = pathlib.Path(source_dir, filename).expanduser().resolve()
        if replace and file_path.suffix == ".png":
            # copy to output dir
            shutil.copy(file_path, pathlib.Path(output_dir) / file_path.with_suffix(".png").name)
            continue
        
        with Image.open(str(file_path)) as img:
            # Define the new filename with PNG extension
            if replace:
                new_file_path = file_path.with_suffix(".png")
                img.convert('RGB').save(new_file_path, 'PNG')
                os.remove(file_path)
            else:
                new_file_path = pathlib.Path(output_dir) / file_path.with_suffix(".png").name
                img.convert('RGB').save(new_file_path, 'PNG')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert all images in a directory to PNG format.")
    parser.add_argument("directory", help="Directory containing the images to be converted")
    parser.add_argument("--replace", 
        help="Delete old files after converting?", 
        action='store_true', 
        default=False  
    )

    args = parser.parse_args()
    input_dir = args.directory
    convert_images_to_png(input_dir, replace=args.replace)
   