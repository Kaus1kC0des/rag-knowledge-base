# schemas/__init__.py

"""
Initializes the schemas module, making document models easily importable.
"""

from .subject import Subject
from .unit import Unit
from .source_document import SourceDocument
from .chunk import Chunk

__beanie_models__ = [Subject, Unit, SourceDocument, Chunk]