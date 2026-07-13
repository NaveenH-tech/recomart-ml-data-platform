from pathlib import Path


def create_directory(path: str):

    Path(path).mkdir(parents=True, exist_ok=True)


def file_exists(path: str):

    return Path(path).exists()
