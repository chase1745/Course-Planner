from course import Course
from section import Section
from itertools import product


def generate_schedules(section_list):
    scheduleList = []
    schedulePossible = True

    for schedule in product(*section_list):
        for sec in schedule:
            if not schedulePossible:
                break
            for sec2 in schedule:
                if sec is not sec2 and sec.interfere(sec2):
                    schedulePossible = False
        if schedulePossible:
            scheduleList.append(schedule)
        else: 
            schedulePossible = True

    return scheduleList    


def main():
    course1 = Course("CSCE", "181")
    sec1 = Section("CSCE", "181", "500", "3:55PM", "5:10pm", "TR")
    sec2 = Section("CSCE", "181", "002", "9:00pm", "9:50pm", "MWF")
    section_list = [sec1, sec2]
    [course1.addSection(sec) for sec in section_list]

    course2 = Course("CSCE", "313")
    sec3 = Section("CSCE", "313", "505", "11:10am", "12:25pm", "TR")
    sec4 = Section("CSCE", "313", "004", "9:00am", "9:50am", "TR")
    section_list = [sec3, sec4]
    [course2.addSection(sec) for sec in section_list]

    course3 = Course("CSCE", "314")
    sec5 = Section("CSCE", "314", "502", "10:00am", "10:50pm", "MWF")
    sec6 = Section("CSCE", "314", "503", "9:30am", "11:50am", "TR")
    section_list = [sec5, sec6]
    [course3.addSection(sec) for sec in section_list]

    course4 = Course("MATH", "304")
    sec8 = Section("MATH", "304", "502", "9:10am", "9:50am", "MWF")
    section_list = [sec8]
    [course4.addSection(sec) for sec in section_list]

    course5 = Course("ENGL", "204")
    sec9 = Section("ENGL", "204", "999", "8:10am", "8:50am", "MWF")
    section_list = [sec9]
    [course5.addSection(sec) for sec in section_list]

    course_list = [course1, course2, course3, course4, course5]

    # Create section list to use in itertools's product function
    sec_list = [courses.getSections() for courses in course_list]
    scheduleList = generate_schedules(sec_list)    

    i = 1
    for schedule in scheduleList:
        print("Schedule", i, ":")
        i += 1
        for section in list(schedule):
            print(section.secInfo)


if __name__ == "__main__":
    main()