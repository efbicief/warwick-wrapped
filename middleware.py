from dataFormat import User, SVG, Category, ThreePart, FivePart, Image,Page
from functools import reduce
import sso
from pprint import pprint as bigpp
from datetime import datetime
import human_readable as hr

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

@defaultWrapFac(None)
def module_cw_mark(ass):
    module = ass['module']['name']
    cw_name = ass['name']
    mark = ass['feedback']['mark']
    if module == None or cw_name == None or mark == None:
        return None
    
    return (module, cw_name, mark)

@defaultWrapFac(None)
def pack_deadlines(ass):
    module = ass['module']['name']
    cw_name = ass['name']
    due = datetime.fromisoformat(ass['closeDate'])
    your_due = datetime.fromisoformat(ass['studentDeadline'])
    submitted = datetime.fromisoformat(ass['submission']['submittedDate'])
    isLate = ass['submission'].get('late', False)
    if module == None or cw_name == None or due == None or your_due == None or submitted == None or isLate == None:
        return None
    
    return (module, cw_name, due, your_due, submitted, isLate)


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
    

"""Get the number of upcoming assignments from assignments"""
def num_upcoming_ass(upcoming_ass)->ThreePart:
    return ThreePart("You have", len(upcoming_ass), "upcoming assignments")

"""Get the number of completed assignments from assignments
    @returns ThreePart data type displying the /You have completed * assignments/"""
def num_completed_ass(completed_ass)->ThreePart:
    return ThreePart("You have", len(completed_ass), "completed assignments")


"""Get the average marks for all submitted assignments 
    @marks a list of [Module, Assignment, Mark] tuples
    @returns ThreePart data type displying the /You have completed * assignments/"""
def avg_mark(marks:list[tuple[int,str,str]])->ThreePart:
    mark_sum = round(reduce(lambda a,b:a+b[2],marks,0)/len(marks),1)
    return ThreePart("Your average mark was", mark_sum, "")

"""Get the largest marks for all submitted assignments 
    @marks a list of [Module, Assignment, Mark] tuples
    @returns ThreePart data type displying the /You have completed * assignments/"""
def max_mark(marks:list[tuple[int,str,str]])->FivePart:
    marks.sort(key=lambda x:x[2])
    return FivePart("Your maximum mark was", marks[-1][2], "For ",marks[-1][1],marks[-1][0])

"""Get the smallest marks for all submitted assignments 
    @marks a list of [Module, Assignment, Mark] tuples
    @returns ThreePart data type displying the /You have completed * assignments/"""
def min_mark(marks:list[tuple[int,str,str]])->FivePart:
    marks.sort(key=lambda x:x[2])
    return FivePart("Your minimum mark was", marks[0][2], "For ", marks[0][1],marks[0][0])


def get_latest_ontime_deadline(deadlines:list[tuple[str,str,datetime,datetime,datetime,bool]])->FivePart:
    ontimes = [ded for ded in deadlines if ded[5] == False]
    ontimes.sort(key=lambda x: x[3]-x[4])
    difference = ontimes[0][3] - ontimes[0][4]
    return FivePart("Your latest on-time submission was", hr.time_delta(difference), "before the deadline for", ontimes[0][1],ontimes[0][0])



def get_data(uuid)-> User:
    member = sso.get_user_info(uuid)
    courseDetails = member.get("studentCourseDetails")[0]
    assignments = sso.get_assignments(uuid)
    upcoming_assignments_aep = assignments.get("enrolledAssignments")
    upcoming_assignments = [ass for ass in upcoming_assignments_aep if "AEP submissions" not in str(ass)]
    completed_assignments_aep = assignments.get("historicAssignments")
    completed_assignments = [ass for ass in completed_assignments_aep if "AEP submissions" not in str(ass)]
    
    # List of (module_name, cw_name, mark) for each completed assignment
    marks_none = [module_cw_mark(ass) for ass in completed_assignments]
    marks = [mark for mark in marks_none if mark is not None]

    # List of (module_name, cw_name, due_date, your_due_date, submitted_date, isLate) for each completed assignment
    deadlines_none = [pack_deadlines(ass) for ass in completed_assignments]
    deadlines = [ded for ded in deadlines_none if ded is not None]

    # Assignments category
    assignment_category = Category(
        "Assignments",
        assignmentsSVG,
        [
            num_upcoming_ass(upcoming_assignments),
            num_completed_ass(completed_assignments),
            min_mark(marks),
            max_mark(marks),
            avg_mark(marks)
        ]
    )

    # Deadlines category
    deadlines_category = Category(
        "Deadlines",
        deadlinesSVG,
        [
            get_latest_ontime_deadline(deadlines)
        ]
    )

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
        [
            assignment_category,
            deadlines_category
        ]
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
