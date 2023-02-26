"""Module for representing a video."""
from dataclasses import dataclass
from typing import Dict


@dataclass
class Video:
    """Video resource instance."""
    id: str
    snippet: Dict[str, str]
    statistic: Dict[str, int]

    def to_dict(self, **kwargs):
        """Convert video instance to dictionary."""
        snippet = {
            "publish_time": self.snippet.get("publishedAt"),
            "category_id": self.snippet.get("categoryId"),
        }
        statistic = {
            "view": self.statistic.get("viewCount"),
            "like": self.statistic.get("likeCount"),
            "comment": self.statistic.get("commentCount")
        }
        video_id = {"video_id": self.id}

        return dict(**video_id, **snippet, **statistic, **kwargs)