from bs4 import BeautifulSoup
import re
from datetime import datetime


def prettify(webData) -> list:
    soup = BeautifulSoup(webData, "html.parser")

    data = []
    for i in soup.find_all(class_="rich-panel-body"):
        course = re.sub(' \(S[1-2](|,S[1-2])\)', '', i.find(class_="dailyGradeCourseNameColumn").get_text())
        grade = re.sub(r'^\xa0$', 'N/A', i.find(class_="dailyGradeGroupColumn").get_text().split(": ")[1]) + '%'
        grade = re.sub(r'[a-zA-Z] ', '', grade)
        assignments = []
        for row in i.find_all(class_="rich-table-row"):
            assignment = {
                'name': row.find(class_="dailyGradeAssignmentColumn").get_text().replace('\n', ''),
                'earned': formatGrade(row.find(class_="dailyGradeScoreColumn").get_text()),
                'possible': formatGrade(row.find(class_="dailyGradePossibleColumn").get_text()),
                'due': row.find(class_="dailyGradeDueDateColumn").get_text(),
            }
            assignment['score'] = '{}/{}'.format(re.sub(r'^\xa0$', '?? ', assignment['earned']), assignment['possible'])

            # adding a year datapoint will most likely be not helpful to anyone
            # using the api, but will reduce calculations here.
            assignment['year'] = assignment['due'].split('/')[-1]

            assignments.append(assignment)
        scores = []

        for x in assignments:
            try:
                if not x['score'].split('/')[0] in ['?? ', 'M', 'E']:
                    x['earned'] = float(x['earned'])
                    x['possible'] = float(x['possible'])
                    scores.append(x)
            except ValueError:
                pass

        dataPoint = {}

        currentYear = str(datetime.now().year)
        currentYearScores = [i for i in scores if
                             i['year'] == currentYear]

        dataPoint['analytics'] = {}

        if len(currentYearScores) > 0:
            dataPoint['analytics']['drop'] = dropAssignments(currentYearScores)
            dataPoint['analytics']['points'] = totalPoints(currentYearScores)
        else:
            dataPoint['analytics']['info'] = 'No assignments found in the current semester to analyze.'


        dataPoint.update({'class': course,
            'grade': grade,
            'earned': sum([float(i['earned']) for i in scores]),
            'possible': sum([float(i['possible']) for i in scores]),
            'assignments': assignments})
        data.append(dataPoint)
    return data

# Some utils for generating avgs and totals

def formatGrade(grade: str) -> str:
    if grade.endswith('.00'):
        return grade.split('.')[0]
    else:
        return grade

# Below here is analytics generation stuff

def dropAssignments(scores: list) -> str:

    keys = [i['earned'] for i in scores]
    values = [i['possible'] for i in scores]

    grade = sum(keys)
    total = sum(values)

    if total == 0:
        return 'Couldn\'t calculate how many points you can afford to lose because there have been 0 total points in the class.'

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


def totalPoints(scores: list) -> str:

    possible = sum([i['earned'] for i in scores])
    total = sum([i['possible'] for i in scores])

    return f"You've earned {possible} points out of {total} points.  {possible} / {total} = {divideTotal(possible, total)}"

def divideTotal(possible: float, total: float):
    if total == 0:
        return 'nevermind, dividing by zero isn\'t possible yet.'
    else:
        return round((possible/total), 4)


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