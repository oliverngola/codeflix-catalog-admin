from dataclasses import dataclass
from uuid import UUID

from src.core.video.domain.value_objects import MediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated:
    aggregate_id: UUID
    media_type: MediaType
    file_path: str