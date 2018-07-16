from bs4 import BeautifulSoup

def prettify(webData):
    soup = BeautifulSoup(webData, "html.parser")

    classes = [i.get_text() for i in soup.find_all(class_="dailyGradeCourseNameColumn")]
    grades = [i.get_text().split(": ")[1] for i in soup.find_all(class_="dailyGradeGroupColumn")]

    return {'classes': classes, 'grades': grades}