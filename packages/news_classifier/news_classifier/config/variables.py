"""
    Module to store the features settings
"""
FEATURES = [
    "category",
    "title",
    "content",
    "topics",
    "published_on"
]

# These features are only used in the data analysis process
DROP_FEATURES = ["title", "topics", "published_on", "category"]

TEXT_FEATURES = ["content"]

TARGET = ["category"]


