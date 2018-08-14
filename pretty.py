from bs4 import BeautifulSoup
import re

def prettify(webData):
    soup = BeautifulSoup(webData, "html.parser")

    data = []

    for i in soup.find_all(class_="rich-panel-body"):
        course = i.find(class_="dailyGradeCourseNameColumn").get_text()
        grade = re.sub(r'^\xa0$', 'N/A', i.find(class_="dailyGradeGroupColumn").get_text().split(": ")[1])
        assignmentNames = [x.get_text() for x in i.find_all(class_="assignmentName")]
        assignmentScores = [x.get_text() for x in i.find_all(class_="points")]
        data.append({
            'class': course,
            'grade': grade,
            'assignments': {assignmentNames[x]: assignmentScores[x] for x in
             range(0, len(assignmentNames))}})
    
    return data