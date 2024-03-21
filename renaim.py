import os, sys
import argparse
from datetime import datetime
from PIL import Image
import base64
import io
import requests
from dotenv import load_dotenv
import json
from typing import List, Dict, Union, Any

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}


def pre_process_files(files: List[str]) -> List[str]:
    """Pre-processes a list of files.

    :param files: A list of file paths.
    :return: A list of clean file paths.

    The method iterates over the provided list of file paths and performs the following checks for each path:
    - If the path is a symbolic link, it is skipped and a message is printed.
    - If the path is a directory, it is skipped and a message is printed.
    - If the file does not have an allowed extension, it is skipped and a message is printed.
    - Otherwise, the file path is added to the clean list.

    The method then returns the clean list of file paths.
    """
    clean_list = []
    for file_path in files:
        if os.path.islink(file_path):
            print(f"Skipping symlink: {file_path}")
            continue
        if os.path.isdir(file_path):
            print(f"Skipping directory: {file_path}")
            continue
        if not allowed_file(file_path):
            print(f"Skipping file with unsupported extension: {file_path}")
            continue
        clean_list.append(file_path)
    return clean_list


def get_creation_date(file_path: str) -> datetime:
    """
    Return the creation date of a file.

    :param file_path: The path of the file.
    :return: Return the creation date of the file as a datetime object.
    """
    if os.name == 'nt':  # Windows
        return datetime.fromtimestamp(os.path.getctime(file_path))
    else:  # Unix/Linux
        stat = os.stat(file_path)
        try:
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            return datetime.fromtimestamp(stat.st_mtime)


def get_image_resolution(file_path: str) -> str:
    """
    :param file_path: The path to the image file.
    :return: A string representing the image resolution in the format "height-width".
    """
    with Image.open(file_path) as img:
        width, height = img.size
        return f"{height}-{width}"


def allowed_file(filename: str) -> bool:
    """
    Check if a file is allowed based on its extension.

    :param filename: The name of the file to check.
    :return: True if the file is allowed, False otherwise.
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def image_to_base64(image_path: str) -> str:
    """
    Converts an image file to its Base64 representation.

    :param image_path: The path of the image file.
    :return: The Base64 representation of the image as a string.

    :raises FileNotFoundError: If the image file does not exist.
    :raises OSError: If there was an error opening or processing the image file.
    """
    with Image.open(image_path) as img:
        img_format = img.format
        buffer = io.BytesIO()
        img.save(buffer, format=img_format)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def process_file(file_path: str, output_dir: str, include_resolution: bool, create_link: bool,
                 timestamp_position: str, generate_description: bool):
    """
    Process and rename a file based on the specified parameters.

    :param file_path: The path of the file to be processed. Ensure it's an absolute path to avoid issues with symlink creation.
    :param output_dir: The directory where the processed file should be outputted. This is converted to an absolute path to ensure symlinks work correctly.
    :param include_resolution: Whether to include the resolution in the new file name for image files.
    :param create_link: Whether to create a symbolic link instead of renaming the file. If a symlink is created, both file_path and output_path are used as absolute paths.
    :param timestamp_position: The position of the timestamp in the new file name ("pre" or "post").
    :param generate_description: Whether to generate a description for the file using AI.

    :return: None
    """

    # Ensure file_path is absolute to avoid issues with symlink creation.
    file_path = os.path.abspath(file_path)

    # Get the base name of the file based on the specified name. Break it into file part and extension.
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    # Determine the date the file was created in case user asked for it.
    creation_date = get_creation_date(file_path)  # Assumes get_creation_date is defined elsewhere
    date_str = creation_date.strftime('%Y-%m-%d')

    # Pass image to AI for processing if requested and the file is allowed.
    if generate_description and allowed_file(file_path):  # Assumes allowed_file is defined elsewhere
        suggested_filename = process_image(file_path)  # Assumes process_image is defined elsewhere
        if suggested_filename:
            name = suggested_filename.rsplit('.', 1)[0]

    # This check becomes straightforward and consistent with allowed_file's logic.
    if include_resolution and ext.lower() in ALLOWED_EXTENSIONS:
        resolution = get_image_resolution(file_path)
        name = f"{name}_{resolution}"

    # Calculate the date format and add before or after filename as specified
    if timestamp_position == 'pre':
        new_name = f"{date_str}_{name}{ext}"
    elif timestamp_position == 'post':
        new_name = f"{name}_{date_str}{ext}"
    else:
        new_name = f"{name}{ext}"

    # Use the specified output directory or the existing directory of the file
    if output_dir:
        output_dir = os.path.abspath(output_dir)  # Convert output_dir to absolute path
        output_path = os.path.join(output_dir, new_name)
    else:
        output_path = os.path.join(os.path.dirname(file_path), new_name)

    try:
        if create_link:
            # Check and remove existing output_path if necessary to avoid symlink creation errors.
            if os.path.exists(output_path) or os.path.islink(output_path):
                os.remove(output_path)
            os.symlink(file_path, output_path)
            print(f"*** sym ***: {base_name} -> {output_path}")
        else:
            os.rename(file_path, output_path)
            print(f"*** mov ***: {base_name} -> {new_name}")
    except FileExistsError:
        print(f"*** err ***: {output_path} exists. Skipping.")
    except OSError as e:
        print(f"*** err ***:  {file_path}: {e}")


def process_image(image_path: str) -> Union[str, None]:
    """
    :param image_path: The path to the image file.
    :return: Either a suggested filename for the image or None if there was an error or the file type is not allowed.

    This method processes an image by converting it to base64 format and sending it to the OpenAI API for text generation. The generated text is then used to suggest a filename for the image
    * based on certain rules.

    The method first checks if the file type of the image is allowed using the `allowed_file` function. If the file type is not allowed, it prints a message and returns None.

    If the file type is allowed, the method proceeds to process the image. It gets the base64 representation of the image using the `image_to_base64` function. It then calls a nested function
    * `get_image_text` to send the image to the OpenAI API for text generation.

    The `get_image_text` function sends a JSON payload to the OpenAI API containing the base64 image and a prompt text. It receives a response from the API and extracts the suggested filename
    * from the response. The suggested filename is constructed by concatenating the generated text with the original file extension.

    If the API call is successful (status code 200), the suggested filename is returned. If there is an error during the API call or the response status code is not 200, an appropriate error
    * message is printed and None is returned.

    Note: This method requires the `os`, `requests`, `json`, and `Union` imports to be present in the code.
    """
    if not allowed_file(image_path):
        print("*** err ***: File type not allowed.")
        return None

    filename: str = os.path.basename(image_path)

    def get_image_text(base64_image: str, filename: str) -> Union[str, None]:
        prompt_text: str = """
            Generate a descriptive filename for this image using a valid filename. Follow these rules:
            * DO NOT add any extension to the filename
            * DO NOT use words like: [in, a, the, with, an]
            * DO be brief but clear
            * DO use _ between words: like_this_example"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                suggested_filename = response.json()['choices'][0]['message']['content'].strip() + f".{filename.split('.')[-1]}"
                return suggested_filename.lower()
            else:
                print(f"Error processing image with OpenAI: HTTP Status Code {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    base64_image = image_to_base64(image_path)
    return get_image_text(base64_image, filename)


def main():
    """
    The main function of the program.

    This function parses the command-line arguments, sets the OpenAI API Key if provided,
    checks for a valid API key, creates the output directory if specified,
    and processes the files.

    :return: None
    """
    parser = argparse.ArgumentParser(description='Rename files or create symlinks with optional timestamp, resolution, and AI-generated descriptions.')
    parser.add_argument('-o', '--out', help='Output directory')
    parser.add_argument('-k', '--api-key', help='Your OpenAI API Key')
    parser.add_argument('-r', '--resolution', action='store_true', help='Include resolution for image files')
    parser.add_argument('-l', '--link', action='store_true', help='Create symlinks instead of renaming')
    parser.add_argument('-ts', '--timestamp', choices=['pre', 'post'], help='Append timestamp before or after the filename')
    parser.add_argument('-d', '--description', action='store_true', help='Generate descriptive filenames using OpenAI')
    parser.add_argument('-a', '--all', action='store_true', help='Process all files, not just those with allowed extensions')
    parser.add_argument('-pre', '--prefix', type=str, dest='prefix', help='Add any custom prefix to the filename')
    parser.add_argument('-post', '--suffix', type=str, dest='suffix', help='Add any custom prefix to the filename')
    parser.add_argument('files', nargs='+', help='Files to process')
    args = parser.parse_args()
    
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key
        print(f"Using API Key: { os.getenv("OPENAI_API_KEY")}")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("No valid API key found. Rerun with -k option or set the environment variable")
        sys.exit()

    output_dir = args.out
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files_to_process = pre_process_files(args.files)

    print(f"*** pre ***: Processing {len(files_to_process)} files...")
    
    for file_path in files_to_process:        
        process_file(file_path, output_dir, args.resolution, args.link, args.timestamp, args.description)


if __name__ == '__main__':
    main()
