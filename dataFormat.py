
class SVG():
    file:str

class DisplayItem:
    size:int
    def getSize(self):
        return self.size
class Category:
    name:str
    image:SVG
    items:list[DisplayItem]

class User:
    name:str
    degree:str
    year_of_study:str
    info:list[Category]
    def __init__(self,uuid) -> None:
        
        self.name="Joseph Evans"
        self.degree="Computer Science"
        self.year_of_study=[
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th",
            "6th",
            "7th"
        ][2] + " Year" 



# e.g.   "You have submitted" "35" "assignments"
class ThreePart(DisplayItem):
    size=1
    def __init__(self,first,second,third) -> None:
        super().__init__()
        self.first = first
        self.second = second
        self.third = third 

# Class for a 5 part data structure
# e.g.   "Your Highest module was" "Databases" "with a total of" "86" "%"
class FivePart(DisplayItem):
    size=1.3

    first:str
    second:str
    third:str
    fourth:str
    fith:str
    def __init__(self,first,second,third,fourth,fith) -> None:
        super().__init__()
        self.first=first
        self.second=second
        self.third=third
        self.fourth=fourth
        self.fith = fith

#Class for generc images
class Image(DisplayItem):
    size=2

    url:str
    def __init__(self,url) -> None:
        super().__init__()
        self.url = url

