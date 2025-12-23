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
-   `streamlit_app.py`: A full-featured web interface to manage your File Search stores, upload documents (with chunking configuration), and chat with your data using citations.

## Streamlit Web App (Recommended)

The easiest way to interact with Gemini File Search is through the included Streamlit app.

### Features
-   **Visual Store Management**: Create, view, and delete file stores.
-   **Easy Uploads**: Drag & drop file uploads with progress tracking.
-   **Advanced Chunking**: Configure chunk size and overlap for your documents during upload.
-   **Interactive Chat**: Query your document stores and receive answers with **citations** (including text excerpts and metadata).
-   **Secure**: API Key is handled securely via environment variables or session input.

### How to Run
1.  Ensure you have the requirements installed:
    ```powershell
    pip install -r requirements.txt
    ```
2.  Run the app:
    ```powershell
    streamlit run streamlit_app.py
    ```
3.  The app will open in your browser. If you don't have `GOOGLE_API_KEY` set in your environment (`.env`), you will be prompted to enter it in the sidebar.

## CLI Scripts Usage

If you prefer using command-line scripts:

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

## Safety & Security

-   **API Keys**: Never commit your `.env` file or hardcode your API key. The `.gitignore` is set up to exclude `.env` and Python virtual environments.
-   **Data Privacy**: Files uploaded to Gemini File Search are stored by Google. Please refer to Google's data privacy policies regarding the Gemini API.
-   **Clean Up**: File Search stores are persistent. Use the app or `delete_file_stores.py` to remove data when you are done to avoid confusing overlap or unnecessary storage.
