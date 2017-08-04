from flask import Flask, render_template, request, jsonify

from datetime import time
from collections import defaultdict

from course import Course
from section import Section
from datetime import time
from itertools import product

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = "Barrett12"

@app.route('/')
def input():
    return render_template('input.html')


@app.route('/output', methods = ['POST'])
def output():
    f = request.form
    departments = f.getlist('department')
    courseNums = f.getlist('courseNum')
    secNums = f.getlist('secNum')
    startTimes = f.getlist('startTime')
    finishTimes = f.getlist('finishTime')
    days = get_days(f)
    secs = f.getlist('sec-indicator')

    print(departments, courseNums, secNums, startTimes, finishTimes, days, secs)

    course_list = []
    i = 0
    for num_secs in secs:
        c = Course(departments[i], courseNums[i])
        course_list.append(c)
        for sections in range(int(num_secs)): 
            s = Section(c.department, c.courseNum, secNums[sections+i], startTimes[sections+i], finishTimes[sections+i], days[sections+i])
            c.addSection(s)
        i += 1

    section_list = [courses.getSections() for courses in course_list]
    scheduleList = generate_schedules(section_list)
    print(len(scheduleList))

    i = 1
    for schedule in scheduleList:
        print("Schedule" + str(i) + ":")
        i += 1
        for section in list(schedule):
            print(section.secInfo)

    return render_template('output.html')

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
            i+=1
    return days

def generate_schedules(section_list):
    scheduleList = []
    schedulePossible = True

    for schedule in product(*(section_list)):
        for sec in schedule:
            if not schedulePossible: 
                break
            for sec2 in schedule:
                if sec != sec2 and sec.interfere(sec2):
                    schedulePossible = False
        if schedulePossible:
            scheduleList.append(schedule)
        else: 
            schedulePossible = True

    return scheduleList 

app.run(debug=True)












