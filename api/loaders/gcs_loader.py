from typing import List, Dict, Optional
from google.cloud import storage
from langchain_google_community.gcs_file import GCSFileLoader
from langchain_google_community.gcs_directory import GCSDirectoryLoader
from langchain_core.documents import Document
from dotenv import load_dotenv
from typing import List, Dict, Optional

from dotenv import load_dotenv
from google.cloud import storage
from langchain_core.documents import Document
from langchain_google_community.gcs_directory import GCSDirectoryLoader
from langchain_google_community.gcs_file import GCSFileLoader

load_dotenv()

def get_all_files_from_bucket(
        bucket_name: str,
        project_name: str
) -> Dict[str, str]:
    """
    Retrieves all files from a Google Cloud Storage bucket.

    This function connects to a GCS bucket and returns a dictionary mapping
    of all blob names to their respective public URLs.

    Args:
        bucket_name: Name of the GCS bucket to access
        project_name: GCP project ID that contains the bucket

    Returns:
        Dictionary mapping blob names (file paths) to their public URLs

    Example:
        ```python
        files = await get_all_files_from_bucket("my-bucket", "my-project")
        for file_name, url in files.items():
            print(f"{file_name}: {url}")
        ```
    """
    client = storage.Client(project=project_name)
    blobs = list(client.list_blobs(bucket_or_name=bucket_name))
    file_map = {}
    for blob in blobs:
        if not blob.name.endswith("/"):
            file_map[blob.name] = blob.public_url
    return file_map


async def load_gcs_file(
        project_name: str,
        bucket_name: str,
        blob_name: str
) -> List[Document]:
    """
    Loads a single file from Google Cloud Storage and converts it to LangChain documents.

    This function creates a GCSFileLoader for the specified blob and loads its content
    asynchronously, returning the resulting documents.

    Args:
        project_name: GCP project ID that contains the bucket
        bucket_name: Name of the GCS bucket to access
        blob_name: Path to the specific file (blob) to load

    Returns:
        List of LangChain Document objects containing the file content and metadata

    Example:
        ```python
        docs = await load_gcs_file(
            "my-project",
            "my-bucket",
            "path/to/document.pdf"
        )
        print(f"Loaded {len(docs)} documents")
        ```
    """
    loader = GCSFileLoader(
        project_name=project_name,
        bucket=bucket_name,
        blob=blob_name
    )
    docs = await loader.aload()
    return docs


async def load_gcs_directory(
        project_name: str,
        bucket_name: str,
        prefix: Optional[str] = None
) -> List[Document]:
    """
    Loads multiple files from a GCS directory and converts them to LangChain documents.

    This function creates a GCSDirectoryLoader for the specified bucket and optional
    prefix (directory path), then loads all matching files asynchronously, returning
    the resulting documents.

    Args:
        project_name: GCP project ID that contains the bucket
        bucket_name: Name of the GCS bucket to access
        prefix: Optional path prefix to filter files (like a folder path)

    Returns:
        List of LangChain Document objects containing the content and metadata
        of all files in the directory

    Example:
        ```python
        # Load all files in the "data" directory
        docs = await load_gcs_directory(
            "my-project",
            "my-bucket",
            "data/"
        )
        print(f"Loaded {len(docs)} documents from directory")
        ```
    """
    loader = GCSDirectoryLoader(
        project_name=project_name,
        bucket=bucket_name,
        prefix=prefix
    )
    docs = await loader.aload()
    return docs

