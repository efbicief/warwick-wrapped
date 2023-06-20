from dataclasses import dataclass
from typing import ClassVar

@dataclass
class SVG():
    file:str

@dataclass
class DisplayItem:
    """An itsm representing a piece of information to be displayed on the page."""
    size:ClassVar[float]
    TYPE:ClassVar[str]
    def getSize(self)->float:
        return self.size

# e.g. "Exams", "Modules", "Courseworks", "Deadlines" etc.
@dataclass
class Category:
    """A group of information collected under a header and icon."""
    name:str
    image:SVG
    items:list[DisplayItem]

@dataclass
class User:
    """A user's information containing all the information to display on the page."""
    name:str
    degree:str
    year_of_study:str
    info:list[Category]


@dataclass
class ThreePart(DisplayItem):
    """A three part data structure. e.g. 'You have submitted" "35" "assignments' """
    first:str
    second:str
    third:str
    size=1
    TYPE="ThreePart"

@dataclass
class FivePart(DisplayItem):
    """a five part data structure. e.g. 'Your Highest module was Databases with a total of 86 %'"""
    first:str
    second:str
    third:str
    fourth:str
    fith:str
    size=1.3
    TYPE="FivePart"

@dataclass
class Image(DisplayItem):
    """Class for generic images usiually charts"""
    url:str
    size=2.5
    TYPE="Image"

@dataclass
class Page(DisplayItem):
    """Used for templating do not use"""
    info:list[Category]
    size=1
    TYPE="Page"
