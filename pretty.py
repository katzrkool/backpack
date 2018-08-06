from bs4 import BeautifulSoup

def prettify(webData):
    soup = BeautifulSoup(webData, "html.parser")

    classes = [i.get_text() for i in soup.find_all(class_="dailyGradeCourseNameColumn")]
    grades = [i.get_text().split(": ")[1] for i in soup.find_all(class_="dailyGradeGroupColumn")]

    assignments = []

    for i in soup.find_all(class_="course"):
        assignmentNames = [x.get_text() for x in i.find_all(class_="assignmentName")]
        assignmentScores = [x.get_text() for x in i.find_all(class_="points")]
        assignments.append({assignmentNames[x]: assignmentScores[x] for x in range(0, len(assignmentNames))})

    data = [{'class': classes[i], 'grade': grades[i], 'assignments': assignments[i]} for i in range(0, len(classes))]

    return data