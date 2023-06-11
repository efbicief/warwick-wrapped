from dataclasses import dataclass

@dataclass
class SVG():
    file:str

@dataclass
class DisplayItem:
    size:int
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
    size=1
    first:str
    second:str
    third:str

# Class for a 5 part data structure
# e.g.   "Your Highest module was" "Databases" "with a total of" "86" "%"
@dataclass
class FivePart(DisplayItem):
    size=1.3

    first:str
    second:str
    third:str
    fourth:str
    fith:str

#Class for generc images
@dataclass
class Image(DisplayItem):
    size=2
    url:str

