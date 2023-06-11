from dataFormat import User
import sso

def get_data(uuid)-> User:
    member = sso.get_user_info(uuid)
    courseDetails = member.get("studentCourseDetails")[0]
    return User(
        member.get("firstName"),
        courseDetails.get("currentRoute").get("name"),
        courseDetails.get("levelCode", 0),
        []
    )

def get_temp_data(uuid)-> User:
    pass
