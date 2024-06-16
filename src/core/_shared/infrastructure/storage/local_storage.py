from pathlib import Path
from src.core._shared.infrastructure.storage.abstract_storage import AbstractStorage


class LocalStorage(AbstractStorage):
    TMP_BUCKET = "/tmp/codeflix-storege"

    def __init__(self, bucket: str = TMP_BUCKET) -> None:
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def storage(self, file_path: str, content: bytes, content_type: str):
        full_path = self.bucket / file_path

        if not full_path.parent.exists():
            full_path.parent.mkdir(parents=True)

        with open(full_path, "wb") as file:
            file.write(content)

        return full_path.as_uri()

    def retrieve(self, file_path: Path) -> bytes:
        with open(self.bucket.joinpath(file_path), "rb") as file:
            return file.read()