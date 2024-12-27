"""A set of tools for handling data."""

from __future__ import annotations

import os
import zipfile

import requests


def download_and_extract_zip(url: str, extract_to: str) -> None:
    """
    Download a ZIP file and extracts it to the given directory.

    Parameters
    ----------
    url : str
        The URL of the ZIP file to download.
    extract_to : str
        The directory where the ZIP file contents will be extracted.
    """
    # Ensure the target directory exists
    os.makedirs(extract_to, exist_ok=True)

    # Define the local path for the downloaded file
    zip_file_path = os.path.join(extract_to, 'downloaded_file.zip')

    print('Downloading ZIP file...')
    # Download the ZIP file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f'File downloaded successfully: {zip_file_path}')
    else:
        raise Exception(
            f'Failed to download file: {response.status_code}, {response.reason}'
        )

    print('Extracting ZIP file...')
    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f'Files extracted to: {extract_to}')

    # Optionally remove the ZIP file after extraction
    os.remove(zip_file_path)
    print('Temporary ZIP file removed.')
