from flask import Flask, render_template, request

from collections import defaultdict

from course import Course
from section import Section
from itertools import product

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def input():
    return render_template('input.html')


@app.route('/output', methods =['POST', 'GET'])
def output():
    f = request.form
    departments = f.getlist('department')
    courseNums = f.getlist('courseNum')
    secNums = f.getlist('secNum')
    startTimes = f.getlist('startTime')
    finishTimes = f.getlist('finishTime')
    days = get_days(f)
    secs = f.getlist('sec-indicator')

    # print(departments, courseNums, secNums, startTimes, finishTimes, days, secs)

    # Remove blank inputs
    section = 0
    course = 0
    coursesToDelete = []
    sectionsToDelete = []
    # Remove blank courses
    for num_secs in secs:
        if departments[course] == '' and courseNums[course] == '':
            coursesToDelete.append(course)
            for sections in range(int(num_secs)):
                sectionsToDelete.append(section)
                section += 1
            course += 1
        else:
            for sections in range(int(num_secs)):
                section += 1
            course += 1
    # print(coursesToDelete, sectionsToDelete)
    for c in reversed(coursesToDelete):
        del departments[c]
        del courseNums[c]
        del secs[c]
    for s in reversed(sectionsToDelete):
        del secNums[s]
        del startTimes[s]
        del finishTimes[s]
    # print(departments, courseNums, secNums, startTimes, finishTimes, days, secs)

    # Remove blank sections
    s = 0
    c = 0
    blankSecNum = 1
    sectionsToDelete = []
    for num_secs in secs:
        for sections in range(int(num_secs)):
            if secNums[s] == '' and startTimes[s] == '' and finishTimes[s] == '' and s not in days:
                # Completely blank section
                sectionsToDelete.append((s, c))
            elif startTimes[s] == '' or finishTimes[s] == '' or s not in days:
                # Input ERROR
                # render_template('input.html')
                sectionsToDelete.append((s, c))
            elif secNums[s] == '':
                # Insert number for section number if left blank
                secNums[s] = str(blankSecNum)
                blankSecNum += 1
            s += 1
        c += 1
    for s in reversed(sectionsToDelete):
        # s[0] == section number, s[1] == course number
        del secNums[s[0]]
        del startTimes[s[0]]
        del finishTimes[s[0]]
        secs[s[1]] = str(int(secs[s[1]]) - 1)
    coursesToDelete = []
    i = 0
    for s in secs:
        # print(s)
        if s == '0': coursesToDelete.append(i)
        i += 1
    for c in reversed(coursesToDelete):
        del secs[c]

    print(departments, courseNums, secNums, startTimes, finishTimes, days, secs)

    # Create sections
    course_list = []
    section = 0
    course = 0
    for num_secs in secs:
        c = Course(departments[course], courseNums[course])
        course_list.append(c)
        for sections in range(int(num_secs)):
            s = Section(c.department,
                        c.courseNum,
                        secNums[section],
                        startTimes[section],
                        finishTimes[section],
                        days[section]
                        )

            c.addSection(s)
            section += 1
        course += 1

    # Find all possible schedules
    section_list = [courses.getSections() for courses in course_list]
    for l in section_list:
        for sec in l:
            print(sec.secInfo, sec.outputInfo['size'], sec.outputInfo['topMargin'])
    scheduleList = generate_schedules(section_list)
    # print("NUMBER OF SCHEDULES:", len(scheduleList))

    # Print schedules
    # i = 1
    # for schedule in scheduleList:
    #     print("Schedule" + str(i) + ":")
    #     i += 1
    #     for section in list(schedule):
    #         print(section.secInfo)

    # Prep data for user output
    # Each schedule in outputScheduleList is a dict with keys: M,T,W,R,F
    #   with values holding the section information.
    outputScheduleList = []
    for schedule in scheduleList:
        s = defaultdict(list)
        s['M'] = []
        s['T'] = []
        s['W'] = []
        s['R'] = []
        s['F'] = []

        for section in list(schedule):
            for day, value in section.days.items():
                if value:
                    s[day].append(section.outputInfo)
        outputScheduleList.append(s)

    return render_template('output.html', scheduleList=outputScheduleList)


def get_days(f):
    M = f.getlist('m')
    T = f.getlist('t')
    W = f.getlist('w')
    R = f.getlist('r')
    FR = f.getlist('f')
    days_html = [M,T,W,R,FR]
    days = defaultdict(str)
    for day in days_html:
        i = 0
        for sec in day:
            if sec == "1":
                if day is M: day_name = "M"
                if day is T: day_name = "T"
                if day is W: day_name = "W"
                if day is R: day_name = "R"
                if day is FR: day_name = "F"
                days[i] += day_name
            i += 1
    return days


def generate_schedules(section_list):
    scheduleList = []
    schedulePossible = True

    for schedule in product(*section_list):
        for sec in schedule:
            if not schedulePossible:
                break
            for sec2 in schedule:
                if sec is not sec2 and sec.interfere(sec2):
                    # print(sec, sec2, 'INTERFERE')
                    schedulePossible = False
        if schedulePossible:
            scheduleList.append(schedule)
        else:
            schedulePossible = True

    return scheduleList


# app.run(debug=True)












