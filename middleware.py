from dataFormat import User
import sso
from pprint import pprint as bigpp

def defaultWrapFac(default):
    def safeWrapper(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return default
        return wrap
    return safeWrapper

@defaultWrapFac(False)
def isSubmissionLate(ass):
    return ass.get('submission', dict()).get('late', False)


def get_data(uuid)-> User:
    member = sso.get_user_info(uuid)
    courseDetails = member.get("studentCourseDetails")[0]
    assignments = sso.get_assignments(uuid)
    upcoming_assignments = assignments.get("enrolledAssignments")
    completed_assignments = assignments.get("historicAssignments")

    # Number of assignements upcoming
    num_upcoming_ass = len(upcoming_assignments)

    # Number of assignments done
    num_completed_ass = len(completed_assignments)

    # Number of late assignments
    late_ass = list(filter(
        lambda ass: isSubmissionLate(ass),
        completed_assignments
    ))
    num_late_ass = len(late_ass)



    return User(
        member.get("firstName"),
        courseDetails.get("currentRoute").get("name"),
        courseDetails.get("levelCode", 0),
        []
    )

def get_temp_data(uuid)-> User:
    pass
