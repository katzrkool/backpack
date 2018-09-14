from bs4 import BeautifulSoup
import re

def prettify(webData):
    soup = BeautifulSoup(webData, "html.parser")

    data = []
    for i in soup.find_all(class_="rich-panel-body"):
        course = re.sub(' \(S[1-2](|,S[1-2])\)', '', i.find(class_="dailyGradeCourseNameColumn").get_text())
        grade = re.sub(r'^\xa0$', 'N/A', i.find(class_="dailyGradeGroupColumn").get_text().split(": ")[1])
        assignmentNames = [x.get_text().replace('\n', '') for x in i.find_all(class_="dailyGradeAssignmentColumn")]
        assignmentEarned = [formatGrade(x.get_text()) for x in i.find_all(class_="dailyGradeScoreColumn")]
        assignmentPossible = [formatGrade(x.get_text()) for x in i.find_all(class_="dailyGradePossibleColumn")]
        assignmentScores = ['{}/{}'.format(assignmentEarned[i], assignmentPossible[i]) for i in range(0, len(assignmentPossible)) if isFloat(assignmentEarned[i])]

        if len(assignmentScores) == 0 and len(assignmentNames) > 0:
            grade = 'N/A'
        elif len(assignmentScores) > 0:
            grade = genGrade(assignmentScores)
        dataPoint = {}
        if len(assignmentScores) > 0:
            dataPoint['analytics'] = {}
            dataPoint['analytics']['drop'] = dropAssignments(assignmentScores)

        assignmentScores = [
            '{}/{}'.format(re.sub(r'^\xa0$', '?? ', assignmentEarned[i]), assignmentPossible[i]) for i in range(0, len(assignmentPossible))]
        dataPoint.update({'class': course,
            'grade': grade,
            'assignments': {assignmentNames[x]: assignmentScores[x] for x in
             range(0, len(assignmentNames))}})
        data.append(dataPoint)
    
    return data

def isFloat(num) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False

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

    average = str(round((grade / total * 100), 2)) + '%'

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
    elif letterBottom == 0.0:
        return ''
    pointsLost = int((grade * (1 / letterBottom)) - total)
    assignmentsLost = round(pointsLost / avgAssignment, 2)

    return 'You can afford to lose {} points (an average of {} assignments) ' \
           'before dropping {}'.format(pointsLost, assignmentsLost, letters[letterBottom])

letters = {
    0.9: 'to a B',
    0.8: 'to a C',
    0.7: 'to a D',
    0.6: 'to an F',
    0.5: 'below 50%',
    0.4: 'below 40%',
    0.3: 'below 30%',
    0.2: 'below 20%',
    0.1: 'below 10%',
}