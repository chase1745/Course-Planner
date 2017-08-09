from datetime import time
#from section import Section

class Course:
    
    def __init__(self, department, courseNum):
        self.department = department
        self.courseNum = courseNum
        self.section_list = []
        self.str_section_list = []
        self.name = department + " " + courseNum
        self.courseName = department + " " + courseNum

    def __str__(self):
        return self.name

    def addSection(self, section):
        self.section_list.append(section)
        self.str_section_list.append(str(section))

    def getSections(self):
        return self.section_list

    def getStrSections(self):
        return self.str_section_list
