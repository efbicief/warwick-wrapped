from dataFormat import User, SVG, Category, ThreePart, FivePart, Image,Page
from functools import reduce
import sso
from pprint import pprint as bigpp
from datetime import datetime, timedelta
from dateutil.parser import parse
import human_readable as hr
from charts import test_chart

def defaultWrapFac(default):
    def safeWrapper(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return default
        return wrap
    return safeWrapper


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
    due = parse(ass['closeDate'])
    your_due = parse(ass['studentDeadline'])
    submitted = parse(ass['submission']['submittedDate'])
    isLate = ass['submission'].get('late', False)
    if module == None or cw_name == None or due == None or your_due == None or submitted == None or isLate == None:
        return None
    
    return (module, cw_name, due, your_due, submitted, isLate)

@defaultWrapFac(None)
def pack_module(module):
    code = module['module']['code']
    name = module['module']['name']
    year = module['academicYear']
    cats = module['cats']
    mark = module['mark']
    if module == None or name == None or year == None or cats == None or mark == None:
        return None
    
    return (code, name, year, cats, mark)

@defaultWrapFac(('Unknown', True))
def pack_monitoring_point(point):
    print("Point")
    bigpp(point)
    print()
    name = point['point']['name']
    attended = point['state'] == "attended"
    if name == None or attended == None:
        return ('Unknown', True)

    return (name, attended)


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
    

"""Get the number of upcoming assignments from assignments"""
def num_upcoming_ass(upcoming_ass) -> ThreePart:
    return ThreePart("You have", len(upcoming_ass), "upcoming assignments")

"""Get the number of completed assignments from assignments
    @returns ThreePart data type displying the /You have completed * assignments/"""
def num_completed_ass(completed_ass) -> ThreePart:
    return ThreePart("You have", len(completed_ass), "completed assignments")


"""Get the average marks for all submitted assignments 
    @marks a list of [Module, Assignment, Mark] tuples
    @returns ThreePart data type displying the /You have completed * assignments/"""
def avg_mark(marks:list[tuple[int,str,str]]) -> ThreePart:
    mark_sum = round(reduce(lambda a,b:a+b[2],marks,0)/len(marks),1)
    return ThreePart("Your average mark was", mark_sum, "")

"""Get the largest marks for all submitted assignments 
    @marks a list of [Module, Assignment, Mark] tuples
    @returns ThreePart data type displying the /You have completed * assignments/"""
def max_mark(marks:list[tuple[int,str,str]]) -> FivePart:
    marks.sort(key=lambda x:x[2])
    return FivePart("Your maximum mark was", marks[-1][2], "For ",marks[-1][1],marks[-1][0])

"""Get the smallest marks for all submitted assignments 
    @marks a list of [Module, Assignment, Mark] tuples
    @returns ThreePart data type displying the /You have completed * assignments/"""
def min_mark(marks:list[tuple[int,str,str]]) -> FivePart:
    marks.sort(key=lambda x:x[2])
    return FivePart("Your minimum mark was", marks[0][2], "For ", marks[0][1],marks[0][0])

"""Get the latest on-time assignment
    @deadlines a list of [Module, Assignment, Due, Your Due, Submitted, isLate] tuples
    @returns FivePart data type displying the /Your latest on-time submission was * before the deadline for * *"""
def get_latest_ontime_deadline(deadlines:list[tuple[str,str,datetime,datetime,datetime,bool]]) -> FivePart:
    ontimes = [ded for ded in deadlines if ded[5] == False]
    ontimes.sort(key=lambda x: x[3]-x[4])
    difference = ontimes[0][3] - ontimes[0][4]
    return FivePart("Your latest on-time submission was", hr.time_delta(difference), "before the deadline for", ontimes[0][1],ontimes[0][0])

"""Get the number of late submissions
    @deadlines a list of [Module, Assignment, Due, Your Due, Submitted, isLate] tuples
    @returns ThreePart data type displying the /You submitted late * times/"""
def get_num_lates(deadlines:list[tuple[str,str,datetime,datetime,datetime,bool]]) -> ThreePart:
    num_lates = 0
    for ded in deadlines:
        if ded[5]:
            num_lates += 1
    return ThreePart("You submitted late", num_lates, "times")

def avg_before_deadline(deadlines:list[tuple[str,str,datetime,datetime,datetime,bool]]) -> ThreePart:
    time_deltas = [ded[3]-ded[4] for ded in deadlines]
    avg_delta = sum(time_deltas, timedelta(0)) / len(time_deltas)
    return ThreePart("On average you submitted", hr.time_delta(avg_delta), "before the deadline")

def avg_module_mark(modules:list[tuple[str,str,str,float,float]]):
    marks = [i[4] for i in modules]
    avg = round(sum(marks)/len(marks),1)
    return ThreePart("Your average module mark was", avg, "")

def best_module(modules:list[tuple[str,str,str,float,float]]):
    modules.sort(key=lambda x:x[4], reverse=True)
    return FivePart("Your best module was", modules[0][1], "with a mark of", modules[0][4], "")

def worst_module(modules:list[tuple[str,str,str,float,float]]):
    modules.sort(key=lambda x:x[4])
    return FivePart("Your worst module was", modules[0][1], "with a mark of", modules[0][4], "")

def num_modules(modules:list[tuple[str,str,str,float,float]]):
    return ThreePart("In total you completed", len(modules), "modules")

def depts_cats(modules:list[tuple[str,str,str,float,float]], member):
    cats = sum([i[3] for i in modules])
    depts = member.get("touchedDepartments", [""])
    return FivePart("You completed", cats, "CATs across", len(depts), "departments")

def missed_monitoring(points:list[tuple[str,bool]]):
    missed = len([pt for pt in points if not pt[1]])
    return FivePart("You missed", missed, "out of", len(points), "monitoring points")


#@defaultWrapFac(User("Bad User", "BEng Cyber-hacking", "0", []))
def get_data(uuid) -> User:
    member = sso.get_user_info(uuid)
    courseDetails = member.get("studentCourseDetails")[0]
    assignments = sso.get_assignments(uuid)
    begin = courseDetails.get("beginDate", "2023")[:4]
    end = courseDetails.get("endDate", "2023")[:4]
    attendance = sso.get_attendance(int(begin), int(end), uuid)

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
    
    # List of (module_code, module_name, year, cats, mark) for modules
    modules_raw = courseDetails.get("moduleRegistrations")
    modules_none = [pack_module(mod) for mod in modules_raw]
    modules = [mod for mod in modules_none if mod is not None]

    # List of monitoring points and whether they were attended
    monitoring_points = []
    for year in attendance:
        for point in year.get("monitoringPoints", []):
            monitoring_points.append(pack_monitoring_point(point))
    

    # Assignments category
    assignment_category = Category(
        "Assignments",
        assignmentsSVG,
        [
            num_upcoming_ass(upcoming_assignments),
            num_completed_ass(completed_assignments),
            avg_mark(marks),
            min_mark(marks),
            max_mark(marks),
            test_chart(),
            test_chart()
        ]
    )

    # Deadlines category
    deadlines_category = Category(
        "Deadlines",
        deadlinesSVG,
        [
            get_latest_ontime_deadline(deadlines),
            get_num_lates(deadlines),
            avg_before_deadline(deadlines)
        ]
    )

    # Modules Category
    modules_category = Category(
        "Modules",
        modulesSVG,
        [
            avg_module_mark(modules),
            best_module(modules),
            worst_module(modules)
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



    return User(
        member.get("firstName"),
        courseDetails.get("currentRoute").get("name"),
        courseDetails.get("levelCode", 0),
        [
            assignment_category,
            deadlines_category,
            modules_category,
            overview_category
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
            #print(j.TYPE)
            currentPage.append(j)
        pages.append(Page(currentPage))
        i.items=pages
        #print(i)
    return user
