# File Renamer Script (renaim.py)

The File Renamer Script is a versatile Python tool designed to automate the process of renaming files within a directory. It offers a variety of options to customize the renaming process, including adding resolutions for image files, appending creation dates, generating descriptive names using AI, and creating symbolic links instead of renaming.

## Features

This script allows you to:
- Rename files based on their creation date, resolution (for image files), or AI-generated descriptions.
- Create symbolic links to the original files instead of renaming them.
- Process files selectively based on their extensions.

## Requirements

- Python 3.x
- Pillow for image processing
- Requests library for API calls
- dotenv for environment variable management

Ensure all dependencies are installed using pip:

```bash
pip install Pillow requests python-dotenv
```

## Usage

```bash
python renaim.py [options] files
```

### Options
* ```-o, --out``` Specify the output directory where the renamed files or symbolic links will be placed. If not provided, the script operates in the current directory.
* ```-k, --api-key``` Provide your OpenAI API key for generating descriptions. This can also be set as an environment variable OPENAI_API_KEY.
* ```-r, --resolution``` Include the resolution in the filename for image files.
* ```-l, --link``` Create symbolic links to the original files instead of renaming them.
* ```-ts, --timestamp``` Choose where to append the timestamp in the filename. Options are pre (before the name) or post (after the name).
* ```-d, --description``` Use AI to generate a descriptive name for image files. This requires an OpenAI API key.
* ```-a, --all``` Process all files in the provided paths, regardless of their extensions. Non-image file types are skipped for image processing tasks.

### Command Examples
Rename all JPG files in the current directory, including their resolution:

```bash
python renaim.py -r *.jpg
```

Generate AI-based descriptions for image files in a specific directory, placing the output in another directory:

```bash
python renaim.py -d -o /path/to/output /path/to/images/*
```

### Notes on Usage
* Ensure you have the required permissions in the output directory when creating symbolic links or renaming files.
* The AI-generated descriptions rely on the OpenAI API. You must have a valid API key and internet access to use this feature.

## License
This script is released under the GNU Public License. Feel free to use, modify, and distribute it as per the license terms.
