from dataclasses import dataclass
from typing import ClassVar

@dataclass
class SVG():
    file:str

@dataclass
class DisplayItem:
    size:ClassVar[int]
    TYPE:ClassVar[str]
    def getSize(self):
        return self.size

# e.g. "Exams", "Modules", "Courseworks", "Deadlines" etc.
@dataclass
class Category:
    name:str
    image:SVG
    items:list[DisplayItem]

@dataclass
class User:
    name:str
    degree:str
    year_of_study:str
    info:list[Category]




# e.g.   "You have submitted" "35" "assignments"
@dataclass
class ThreePart(DisplayItem):
    first:str
    second:str
    third:str
    size=1
    TYPE="ThreePart"

# Class for a 5 part data structure
# e.g.   "Your Highest module was" "Databases" "with a total of" "86" "%"
@dataclass
class FivePart(DisplayItem):
    first:str
    second:str
    third:str
    fourth:str
    fith:str
    size=1.3
    TYPE="FivePart"

#Class for generc images
@dataclass
class Image(DisplayItem):
    url:str
    size=2
    TYPE="Image"

# Used for templating do not use
@dataclass
class Page(DisplayItem):
    info:list[Category]
    size=1
    TYPE="Page"
