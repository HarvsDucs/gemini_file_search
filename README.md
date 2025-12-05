# Gemini File Search & Store Demo

This repository contains Python scripts demonstrating how to use Google's Gemini API for File Search and File Store operations. This is useful for implementing Retrieval-Augmented Generation (RAG) using your own documents.

## Prerequisites

1.  **Python 3.7+**
2.  **Google Gen AI SDK**: Install the required package using pip:
    ```powershell
    pip install -r requirements.txt
    ```
3.  **API Key**: You need a Google Cloud Project with the Gemini API enabled. Set your API key as an environment variable:
    ```powershell
    $env:GOOGLE_API_KEY="your_api_key_here"
    ```

## Files Description

-   `file_search.py`: Demonstrates how to upload a file (`sample.txt`), create a File Search Store, and query the Gemini model using the uploaded content as context.
-   `check_file_stores.py`: Shows how to create, list, get details of, and delete a File Search Store.
-   `delete_file_stores.py`: A utility script to list and delete *all* existing File Search Stores associated with your project. **Use with caution.**
-   `sample.txt`: A sample text file used by `file_search.py` for demonstration purposes.

## Usage

1.  **Prepare your data**: Ensure `sample.txt` exists or replace it with your own text file.
2.  **Run the search demo**:
    ```powershell
    python file_search.py
    ```
3.  **Manage stores**:
    To check stores:
    ```powershell
    python check_file_stores.py
    ```
    To cleanup all stores:
    ```powershell
    python delete_file_stores.py
    ```

## Notes

-   The `genai.Client()` automatically looks for the `GOOGLE_API_KEY` environment variable.
-   File Search Stores are persistent. Remember to clean them up if they are no longer needed to avoid clutter or potential costs.
