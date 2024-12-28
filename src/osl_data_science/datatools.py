"""A set of tools for handling data."""

from __future__ import annotations

import os
import zipfile

from pathlib import Path

import requests


def download_and_extract_zip(url: str, extract_to: Path) -> None:
    """
    Download a ZIP file and extracts it to the given directory.

    Parameters
    ----------
    url : str
        The URL of the ZIP file to download.
    extract_to : Path
        The directory where the ZIP file contents will be extracted.
    """
    # Ensure the target directory exists
    extract_to.mkdir(parents=True, exist_ok=True)

    # just download the dataset if the data folder is not empty
    if not is_folder_empty(extract_to):
        print('extract_to directory is not empty, skip the data downloading.')
        return

    # Define the local path for the downloaded file
    zip_file_path = extract_to / 'downloaded_file.zip'

    print('Downloading ZIP file...')
    # Download the ZIP file
    response = requests.get(url, stream=True)
    if response.status_code == 200:  # noqa: PLR2004
        with open(zip_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f'File downloaded successfully: {zip_file_path}')
    else:
        raise Exception(
            f'Failed to download: {response.status_code}, {response.reason}'
        )

    print('Extracting ZIP file...')
    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f'Files extracted to: {extract_to}')

    # Optionally remove the ZIP file after extraction
    os.remove(zip_file_path)
    print('Temporary ZIP file removed.')


def is_folder_empty(folder: Path) -> bool:
    """
    Check if the specified folder is empty using pathlib.

    Parameters
    ----------
    folder_path : Path
        The path of the folder to check.

    Returns
    -------
    bool
        True if the folder is empty, False otherwise.
    """
    # Check if the folder exists and is a directory
    if not folder.exists():
        raise FileNotFoundError(f"The folder '{folder}' does not exist.")
    if not folder.is_dir():
        raise NotADirectoryError(f"The path '{folder}' is not a directory.")

    # Check if the folder is empty
    return not any(folder.iterdir())
