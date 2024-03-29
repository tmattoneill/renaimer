
# Renaimer

Renaimer is a versatile Python script designed for file management, specifically focusing on renaming files or creating symbolic links with enhanced features. It integrates a variety of options, including the insertion of timestamps, inclusion of image resolutions, and the utilization of AI-generated descriptions for more descriptive filenames.

## Features

- **Timestamp Insertion:** Optionally insert the file creation timestamp in the filename.
- **Resolution Inclusion:** For image files, include the resolution in the filename.
- **AI-generated Descriptions:** Generate descriptive filenames based on the file content using an AI model from the OpenAI API.
- **Symbolic Link Creation:** Create symbolic links instead of renaming files for non-destructive operations.
- **MD5 Hashing:** Use an MD5 hash of the image data for creating unique filenames.
- **Flexible File Processing:** Process all files in the input directory, including non-image files if desired.

## Requirements

To run this script, you will need Python 3.6 or later and the following packages:

- Pillow
- python-dotenv
- requests

These can be installed via pip:

```bash
pip install Pillow python-dotenv requests
```

## Usage

```bash
python renaimer.py [options] <files>
```

### Options

- `-o`, `--out`: Specify the output directory. Defaults to the original file location if not provided.
- `-k`, `--api-key`: Provide your OpenAI API Key. Required for AI-generated descriptions.
- `-r`, `--resolution`: Include the resolution of image files in their filenames.
- `-l`, `--link`: Create symbolic links instead of renaming.
- `-ts`, `--timestamp`: Append the creation timestamp (`pre` for before the filename, `post` for after).
- `-d`, `--description`: Generate a descriptive filename using AI.
- `-md5`, `--hash`: Use a hash of the image data for the filename. Incompatible with `-d`.
- `-a`, `--all`: Process all files, not just images.
- `-pp`, `--prepend`: Add a custom prefix to the filename.
- `-ap`, `--append`: Add a custom suffix to the filename.

### Arguments

- `files`: The list of files to process. Supports multiple files and wildcards (e.g., `*.jpg`).

## Example

Renaming image files with their resolution, a timestamp prefix, and a custom suffix:

```bash
python renaimer.py -r -ts pre -ap processed *.jpg
```

## Environment Variables

To avoid passing your API key every time, you can set it as an environment variable `OPENAI_API_KEY`.

## Notes

Ensure that the files you wish to process are not read-only and that you have the necessary permissions.

## License

This script is released under the MIT License. See the LICENSE file for more details.
