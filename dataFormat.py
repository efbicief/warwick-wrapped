


class userInfo:
    name:str
    degree:str
    year_of_study:str
    def __init__(self,authInfo) -> None:
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


class UserData:
    info:userInfo

    def __init__(self,authInfo) -> None:
        self.user_info = userInfo(authInfo)

