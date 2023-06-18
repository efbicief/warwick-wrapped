"""Handles the majoirty of the data processing and formatting for the frontend."""
from functools import reduce
from typing import NewType, Union
import uuid as uuidLib

from pprint import pprint as bigpp
from datetime import datetime, timedelta
from dateutil.parser import parse
import human_readable as hr

import sso
from charts import graph_before_deadline, module_grade_histogram
from dataFormat import User, SVG, Category, ThreePart, FivePart,Page
from sso.config import CONFIG

BASE_URL = CONFIG.BASE_URL

CourseworkMark = NewType( "CourseworkMark", tuple[str, str, int])
Deadline = NewType("Deadlines", tuple[str, str, datetime, datetime, datetime, bool])
Module = NewType("Module", tuple[str, str, int, int, int])
MonitoringPoint = NewType("Module", tuple[str, bool])

AssignmentResponce = NewType("Assignment", dict)
ModuleResponce = NewType("Assignment", dict)
PointResponce = NewType("Assignment", dict)

def default_wrap_fac(default):
    """ Decorator factory to wrap a function in a try catch block
        returning a default value if an exception is raised"""
    def safe_wrapper(func):
        """Decorator to wrap a function in a try catch block"""
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default
        return wrap
    return safe_wrapper

@default_wrap_fac(None)
def module_cw_mark(ass:AssignmentResponce)->Union[CourseworkMark,None]:
    """For a given assignemnt extrace the module, assignment name and mark"""
    module:str = str(ass['module']['name'])
    cw_name:str = str(ass['name'])
    mark:int = int(ass['feedback']['mark'])
    if module is None or cw_name is None or mark is None:
        return None
    return CourseworkMark((module, cw_name, mark))

@default_wrap_fac(None)
def pack_deadlines(ass:AssignmentResponce)->Union[Deadline,None]:
    """For a given assignment extract the relevent daeadlne information as a tuple
        Module name
        Coursework Name
        Due date (exclusive of alowances)
        Due date (inclusive of alowances)
        Submitted date
        is late , boolean flag """
    module = ass['module']['name']
    cw_name = ass['name']
    due = parse(ass['closeDate'])
    your_due = parse(ass['studentDeadline'])
    submitted = parse(ass['submission']['submittedDate'])
    is_late = ass['submission'].get('late', False)
    if module is None or cw_name is None or due is None:
        return None
    if your_due is None or submitted is None or is_late is None:
        return None
    return Deadline((module, cw_name, due, your_due, submitted, is_late))

@default_wrap_fac(None)
def pack_module(module:ModuleResponce)->Union[Module,None]:
    """  For a given module extract the relevent  """
    code = module['module']['code']
    name = module['module']['name']
    year = module['academicYear']
    cats = module['cats']
    mark = module['mark']
    if module is None or name is None or year is None or cats is None or mark is None:
        return None
    return Module((code, name, year, cats, mark))

@default_wrap_fac(('Unknown', True))
def pack_monitoring_point(point:PointResponce)->MonitoringPoint:
    """Check monitoring points by name and attendance"""
    name = point['point']['name']
    attended = point['state'] == "attended"
    if name is None or attended is None:
        return MonitoringPoint(('Unknown', True))

    return MonitoringPoint((name, attended))


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

modulesSVG = SVG("""
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-menu-button-wide-fill" viewBox="0 0 16 16">
  <path d="M1.5 0A1.5 1.5 0 0 0 0 1.5v2A1.5 1.5 0 0 0 1.5 5h13A1.5 1.5 0 0 0 16 3.5v-2A1.5 1.5 0 0 0 14.5 0h-13zm1 2h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1 0-1zm9.927.427A.25.25 0 0 1 12.604 2h.792a.25.25 0 0 1 .177.427l-.396.396a.25.25 0 0 1-.354 0l-.396-.396zM0 8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8zm1 3v2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2H1zm14-1V8a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v2h14zM2 8.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5zm0 4a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5z"/>
</svg>
""")

overviewSVG = SVG("""
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-globe-europe-africa" viewBox="0 0 16 16">
  <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM3.668 2.501l-.288.646a.847.847 0 0 0 1.479.815l.245-.368a.809.809 0 0 1 1.034-.275.809.809 0 0 0 .724 0l.261-.13a1 1 0 0 1 .775-.05l.984.34c.078.028.16.044.243.054.784.093.855.377.694.801-.155.41-.616.617-1.035.487l-.01-.003C8.274 4.663 7.748 4.5 6 4.5 4.8 4.5 3.5 5.62 3.5 7c0 1.96.826 2.166 1.696 2.382.46.115.935.233 1.304.618.449.467.393 1.181.339 1.877C6.755 12.96 6.674 14 8.5 14c1.75 0 3-3.5 3-4.5 0-.262.208-.468.444-.7.396-.392.87-.86.556-1.8-.097-.291-.396-.568-.641-.756-.174-.133-.207-.396-.052-.551a.333.333 0 0 1 .42-.042l1.085.724c.11.072.255.058.348-.035.15-.15.415-.083.489.117.16.43.445 1.05.849 1.357L15 8A7 7 0 1 1 3.668 2.501Z"/>
</svg>
""")

def num_upcoming_ass(upcoming_ass:list[AssignmentResponce]) -> ThreePart:
    """Get the number of upcoming assignments from assignments"""
    return ThreePart("You have", str(len(upcoming_ass)), "upcoming assignments")

def num_completed_ass(completed_ass:list[AssignmentResponce]) -> ThreePart:
    """Get the number of completed assignments from assignments
        @returns ThreePart data type displying the /You have completed * assignments/"""
    return ThreePart("You have", str(len(completed_ass)), "completed assignments")


def avg_mark(marks:list[CourseworkMark]) -> ThreePart:
    """Get the average marks for all submitted assignments 
        @marks a list of [Module, Assignment, Mark] tuples
        @returns ThreePart data type displying the /You have completed * assignments/"""
    mark_sum = round(reduce(lambda a,b:a+b[2],marks,0)/len(marks),1)
    return ThreePart("Your average mark was", str(mark_sum), "")

def max_mark(marks:list[CourseworkMark]) -> FivePart:
    """Get the largest marks for all submitted assignments 
        @marks a list of [Module, Assignment, Mark] tuples
        @returns ThreePart data type displying the /You have completed * assignments/"""
    marks.sort(key=lambda x:x[2])
    return FivePart("Your maximum mark was", str(marks[-1][2]), "For ",marks[-1][1],marks[-1][0])

def min_mark(marks:list[CourseworkMark]) -> FivePart:
    """Get the smallest marks for all submitted assignments 
        @marks a list of [Module, Assignment, Mark] tuples
        @returns ThreePart data type displying the /You have completed * assignments/"""
    marks.sort(key=lambda x:x[2])
    return FivePart("Your minimum mark was", str(marks[0][2]), "For ", marks[0][1],marks[0][0])

def get_latest_ontime_deadline(deadlines:list[Deadline]) -> FivePart:
    """Get the latest on-time assignment
        @deadlines a list of [Module, Assignment, Due, Your Due, Submitted, isLate] tuples
        @returns FivePart data type displying the 
            'Your latest on-time submission was * before the deadline for * * '"""
    ontimes = [dedline for dedline in deadlines if not dedline[5]]
    ontimes.sort(key=lambda x: x[3]-x[4])
    difference = ontimes[0][3] - ontimes[0][4]
    return FivePart("Your latest on-time submission was", 
                    hr.time_delta(difference), 
                    "before the deadline for", 
                    ontimes[0][1],
                    ontimes[0][0])

def get_num_lates(deadlines:list[Deadline]) -> ThreePart:
    """Get the number of late submissions
        @deadlines a list of [Module, Assignment, Due, Your Due, Submitted, isLate] tuples
        @returns ThreePart data type displying the /You submitted late * times/"""
    num_lates = 0
    for ded in deadlines:
        if ded[5]:
            num_lates += 1
    return ThreePart("You submitted late", str(num_lates), "times")

def avg_before_deadline(deadlines:list[Deadline]) -> ThreePart:
    """Get the average time submitted before the deadline"""
    time_deltas = [ded[3]-ded[4] for ded in deadlines]
    time_deltas.sort()
    avg_delta = time_deltas[len(time_deltas)//2]
    # avg_delta = sum(time_deltas, timedelta(0)) / len(time_deltas)
    return ThreePart("On average you submitted", hr.time_delta(avg_delta), "before the deadline")

def avg_module_mark(modules:list[Module]):
    """Get the average module mark from a list of modules"""
    marks = [i[4] for i in modules]
    if len(marks) == 0: avg = 0
    else: avg = sum(marks)/len(marks)
    return ThreePart("Your average module mark was", str(round(avg,1)), "")

def best_module(modules:list[Module]):
    """Get the best module from a list of modules"""
    modules.sort(key=lambda x:x[4], reverse=True)
    return FivePart("Your best module was", modules[0][1], "with a mark of", str(modules[0][4]), "")

def worst_module(modules:list[Module]):
    """Get the worst module from a list of modules"""
    modules.sort(key=lambda x:x[4])
    return FivePart("Your worst module was", modules[0][1], "with a mark of", str(modules[0][4]), "")

def num_modules(modules:list[Module]):
    """Get the number of modules from a list of modules"""
    return ThreePart("In total you completed", str(len(modules)), "modules")

def depts_cats(modules:list[Module], member):
    """Get the total number of CATS completed and the number of departments used"""
    cats = sum([i[3] for i in modules])
    depts = member.get("touchedDepartments", [""])
    return FivePart("You completed", str(cats), "CATs across", str(len(depts)), "departments")

def missed_monitoring(points:list[MonitoringPoint]):
    """Get the number of missed monitoring points from a list of monitoring points"""
    missed = len([pt for pt in points if not pt[1]])
    return FivePart("You missed", str(missed), "out of", str(len(points)), "monitoring points")


#@default_wrap_fac(User("Bad User", "BEng Cyber-hacking", "0", []))
def get_data(uuid) -> User:
    """Get all the data for a user"""
    member = sso.get_user_info(uuid)
    course_details = member.get("studentCourseDetails", [])[-1]
    assignments = sso.get_assignments(uuid)
    begin = course_details.get("beginDate", "2023")[:4]
    end = course_details.get("endDate", "2023")[:4]
    attendance = sso.get_attendance(int(begin), int(end)+1, uuid)

    upcoming_assignments_aep = assignments.get("enrolledAssignments")
    upcoming_assignments = [ass for ass in upcoming_assignments_aep if \
                                            "AEP submissions" not in str(ass)]
    completed_assignments_aep = assignments.get("historicAssignments")
    completed_assignments = [ass for ass in completed_assignments_aep if \
                                            "AEP submissions" not in str(ass)]

    # List of (module_name, cw_name, mark) for each completed assignment
    marks_none = [module_cw_mark(ass) for ass in completed_assignments]
    marks = [mark for mark in marks_none if mark is not None]

    # List of (module_name, cw_name, due_date, your_due_date, submitted_date, isLate)
    # for each completed assignment
    deadlines_none = [pack_deadlines(ass) for ass in completed_assignments]
    deadlines = [ded for ded in deadlines_none if ded is not None]

    # List of (module_code, module_name, year, cats, mark) for modules
    modules_raw = course_details.get("moduleRegistrations", dict())
    modules_none = [pack_module(mod) for mod in modules_raw]
    modules = [mod for mod in modules_none if mod is not None]

    # List of monitoring points and whether they were attended
    monitoring_points = []
    for year in attendance:
        for point in year.get("monitoringPoints", []):
            monitoring_points.append(pack_monitoring_point(point))

    # Assignments category
    if len(marks) == 0:
        assignment_category = None
    else:
        assignment_category = Category(
            "Assignments",
            assignmentsSVG,
            [
                num_upcoming_ass(upcoming_assignments),
                num_completed_ass(completed_assignments),
                avg_mark(marks),
                min_mark(marks),
                max_mark(marks),
            ]
        )

    # Deadlines category
    if len(deadlines) == 0:
        deadlines_category = None
    else:
        deadlines_category = Category(
            "Deadlines",
            deadlinesSVG,
            [
                get_latest_ontime_deadline(deadlines),
                get_num_lates(deadlines),
                avg_before_deadline(deadlines),
                graph_before_deadline(deadlines)
            ]
        )

    # Modules Category
    if len(modules) == 0:
        modules_category = None
    else:
        modules_category = Category(
            "Modules",
            modulesSVG,
            [
                avg_module_mark(modules),
                best_module(modules),
                worst_module(modules),
                module_grade_histogram(modules)
            ]
        )

    # Overview category
    overview_category = Category(
        "Overview",
        overviewSVG,
        [
            num_modules(modules),
            depts_cats(modules, member),
            missed_monitoring(monitoring_points)
        ]
    )


    categories_none = [ assignment_category, deadlines_category, modules_category, overview_category ]
    categories = [c for c in categories_none if c != None]
    return User(
        member.get("firstName", "Unknown first name"),
        course_details.get("currentRoute", dict()).get("name", "Unknown course"),
        course_details.get("levelCode", 0),
        categories
    )




def get_temp_data(uuid:str)-> User:
    """Get all the data for a user (temporary used for testing)"""
    print(uuid)
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
    """Converts the items in the categories to pages A default of 4 units per page"""
    catgories=user.info
    for i in catgories:
        pages=[]
        current_page=[]
        current_page_size=0
        for j in i.items:
            current_page_size+=j.getSize()
            if current_page_size>4:
                pages.append(Page(current_page))
                current_page=[]
                current_page_size=j.getSize()
            current_page.append(j)
        pages.append(Page(current_page))
        i.items=pages
    return user

def get_share_link(uuid:str)->dict:
    """Returns a share link for the user"""
    myuuid = uuidLib.uuid4()
    print(myuuid)
    sso.db_data.add_token_share_code(str(myuuid), uuid)
    print(myuuid)
    return {"link":BASE_URL+"/results?ref="+str(myuuid)}
