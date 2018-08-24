from bs4 import BeautifulSoup
import re

def prettify(webData):
    soup = BeautifulSoup(webData, "html.parser")

    data = []
    for i in soup.find_all(class_="rich-panel-body"):
        course = i.find(class_="dailyGradeCourseNameColumn").get_text().replace(' (S1,S2)', '')
        grade = re.sub(r'^\xa0$', 'N/A', i.find(class_="dailyGradeGroupColumn").get_text().split(": ")[1])
        assignmentNames = [x.get_text().replace('\n', '') for x in i.find_all(class_="dailyGradeAssignmentColumn")]
        assignmentEarned = [formatGrade(x.get_text()) for x in i.find_all(class_="dailyGradeScoreColumn")]
        assignmentPossible = [formatGrade(x.get_text()) for x in i.find_all(class_="dailyGradePossibleColumn")]
        assignmentScores = ['{}/{}'.format(assignmentEarned[i], assignmentPossible[i]) for i in range(0, len(assignmentPossible))]
        if grade == 'N/A' and len(assignmentNames) > 0:
            grade = genGrade(assignmentScores)
        dataPoint = {}
        if len(assignmentNames) > 0:
            dataPoint['analytics'] = {}
            dataPoint['analytics']['drop'] = dropAssignments(assignmentScores)
        dataPoint.update({'class': course,
            'grade': grade,
            'assignments': {assignmentNames[x]: assignmentScores[x] for x in
             range(0, len(assignmentNames))}})
        data.append(dataPoint)
    
    return data

def formatGrade(grade: str):
    if grade.endswith('.00'):
        return grade.split('.')[0]
    else:
        return grade

def genGrade(scores):
    convertedScores = {}
    for i in scores:
        convertedScores[float(i.split('/')[0])] = float(i.split('/')[1])

    grade = sum(convertedScores.keys())
    total = sum(convertedScores.values())

    average = str((grade / total) * 100) + '%'

    return average

def dropAssignments(scores):
    convertedScores = []
    for i in scores:
        convertedScores.append((float(i.split('/')[0]), float(i.split('/')[1])))

    keys = [i[0] for i in convertedScores]
    values = [i[1] for i in convertedScores]

    grade = sum(keys)
    total = sum(values)

    average = (grade/total)
    avgAssignment = total / len(values)
    letterBottom = (int(average*10)/10)
    if letterBottom == 1.0:
        letterBottom = 0.9

    pointsLost = int((grade * (1 / letterBottom)) - total)
    assignmentsLost = round(pointsLost / avgAssignment, 2)

    return 'You can afford to lose {} points (an average of {} assignments) ' \
           'before dropping to a {}'.format(pointsLost, assignmentsLost, letters[letterBottom])

letters = {
    0.9: 'B',
    0.8: 'C',
    0.7: 'D',
    0.6: 'F'
}