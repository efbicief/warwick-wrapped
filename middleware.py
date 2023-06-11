from dataFormat import User, SVG, Category, ThreePart, FivePart, Image,Page
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


deadlinesSVG = SVG("""
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16">
        <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
    </svg>
""")

assignmentsSVG = SVG("""
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-journal-bookmark" viewBox="0 0 16 16">
    <path fill-rule="evenodd" d="M6 8V1h1v6.117L8.743 6.07a.5.5 0 0 1 .514 0L11 7.117V1h1v7a.5.5 0 0 1-.757.429L9 7.083 6.757 8.43A.5.5 0 0 1 6 8z"/>
    <path d="M3 0h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-1h1v1a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1H1V2a2 2 0 0 1 2-2z"/>
    <path d="M1 5v-.5a.5.5 0 0 1 1 0V5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1H1zm0 3v-.5a.5.5 0 0 1 1 0V8h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1H1zm0 3v-.5a.5.5 0 0 1 1 0v.5h.5a.5.5 0 0 1 0 1h-2a.5.5 0 0 1 0-1H1z"/>
    </svg>
""")



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
    categories=[
        Category("Deadlines",deadlinesSVG,[
            ThreePart("You have submitted","35","assignments on time"),
            ThreePart("You have submitted","2","assignments Late"),
            ThreePart("You have used","4","extentions"),
            FivePart("Your Highest module was","Databases","with a total of","86","%"),
        ]),
        Category("Deadlines",deadlinesSVG,[
            ThreePart("You have submitted","35","assignments on time"),
            ThreePart("You have submitted","2","assignments Late"),
            ThreePart("You have used","4","extentions"),
            FivePart("Your Highest module was","Databases","with a total of","86","%"),
        ]),
        Category("Deadlines",deadlinesSVG,[
            ThreePart("You have submitted","35","assignments on time"),
            ThreePart("You have submitted","2","assignments Late"),
            ThreePart("You have used","4","extentions"),
            FivePart("Your Highest module was","Databases","with a total of","86","%"),
        ]),
        Category("Deadlines",deadlinesSVG,[
            ThreePart("You have submitted","35","assignments on time"),
            ThreePart("You have submitted","2","assignments Late"),
            ThreePart("You have used","4","extentions"),
            FivePart("Your Highest module was","Databases","with a total of","86","%"),
        ])
    ]

    user=User("John Smith","Computer Science","2nd Year",categories)
    return user

def convert_to_page(user:User)->User:
    catgories=user.info
    for i in catgories:
        pages=[]
        currentPage=[]
        currentPageSize=0
        for j in i.items:
            currentPageSize+=j.getSize()
            if currentPageSize>4:
                pages.append(Page(currentPage))
                currentPage=[]
                currentPageSize=j.getSize()
            print(j.TYPE)
            currentPage.append(j)
        pages.append(Page(currentPage))
        i.items=pages
        print(i)
    return user
