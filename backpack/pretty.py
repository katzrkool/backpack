from bs4 import BeautifulSoup
import re

def prettify(webData):
    soup = BeautifulSoup(webData, "html.parser")

    data = []
    for i in soup.find_all(class_="rich-panel-body"):
        course = re.sub(' \(S[1-2](|,S[1-2])\)', '', i.find(class_="dailyGradeCourseNameColumn").get_text())
        grade = re.sub(r'^\xa0$', 'N/A', i.find(class_="dailyGradeGroupColumn").get_text().split(": ")[1])
        assignments = []
        for row in i.find_all(class_="rich-table-row"):
            assignment = {
                'name': row.find(class_="dailyGradeAssignmentColumn").get_text().replace('\n', ''),
                'earned': formatGrade(row.find(class_="dailyGradeScoreColumn").get_text()),
                'possible': formatGrade(row.find(class_="dailyGradePossibleColumn").get_text()),
                'due': row.find(class_="dailyGradeDueDateColumn").get_text()
            }
            assignment['score'] = '{}/{}'.format(re.sub(r'^\xa0$', '?? ', assignment['earned']), assignment['possible'])
            assignments.append(assignment)
        scores = [x['score'] for x in assignments]
        convertedScores = []
        missingAssignments = []

        for i in scores:
            try:
                if i.split('/')[0] in ['?? ', 'M']:
                    missingAssignments.append((0, float(i.split('/')[1])))
                else:
                    convertedScores.append((float(i.split('/')[0]), float(i.split('/')[1])))
            except ValueError:
                pass

        if len(convertedScores) == 0 and len(assignments) > 0:
            grade = 'N/A'
        elif len(convertedScores) > 0:
            grade = genGrade(convertedScores + missingAssignments)

        dataPoint = {}
        if len(convertedScores) > 0:
            dataPoint['analytics'] = {}
            dataPoint['analytics']['drop'] = dropAssignments(convertedScores + missingAssignments)
            dataPoint['analytics']['gradeSansMissing'] = genSansMissing(convertedScores)

        dataPoint.update({'class': course,
            'grade': grade,
            'assignments': assignments})
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

def genSansMissing(convertedScores):
    return 'Not counting missing assignments, you have a {}'.format(genGrade(convertedScores))

def genGrade(convertedScores):
    grade = sum([i[0] for i in convertedScores])
    total = sum([i[1] for i in convertedScores])

    average = str(round((grade / total * 100), 2)) + '%'

    return average

def dropAssignments(convertedScores):

    keys = [i[0] for i in convertedScores]
    values = [i[1] for i in convertedScores]

    grade = sum(keys)
    total = sum(values)

    average = (grade/total)
    avgAssignment = total / len(values)
    letterBottom = (int((average+0.005)*10)/10)
    if letterBottom >= 1.0:
        letterBottom = 0.9
    elif letterBottom == 0.0:
        return ''
    letterBottom -= 0.005
    pointsLost = int((grade * (1 / letterBottom)) - total)
    assignmentsLost = round(pointsLost / avgAssignment, 2)

    return 'You can afford to lose {} points (an average of {} assignments) ' \
           'before dropping {}'.format(pointsLost, assignmentsLost, letters[letterBottom])

letters = {
    0.895: 'to a B',
    0.795: 'to a C',
    0.695: 'to a D',
    0.595: 'to an F',
    0.495: 'below 50%',
    0.395: 'below 40%',
    0.295: 'below 30%',
    0.195: 'below 20%',
    0.095: 'below 10%',
}