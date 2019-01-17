import requests
from backpack.errors import AuthError, MyBackpackBrokeError
class Scraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def scrape(self):
        try:
            r = self.session.get(
                '''https://thenewschool.seniormbp.com/SeniorApps/facelets/registration/loginCenter.xhtml?convid=82232''')
        except ConnectionError:
            raise MyBackpackBrokeError()
        try:
            jsessionid = r.cookies['JSESSIONID']
        except KeyError:
            raise MyBackpackBrokeError()

        self.session.header = {
            'cookie': "cookies=true; JSESSIONID={}".format(jsessionid),
            'content-type': "application/x-www-form-urlencoded"
        }
        payload = {'form:signIn':'form:signIn', 'form:userId':self.username, 'form:userPassword': self.password,
                   'AJAXREQUEST':'_viewRoot', 'AJAX:EVENTS_COUNT': '1', 'form':'form', 'javax.faces.ViewState': 'j_id1'}

        try:
            r = self.session.post('''https://thenewschool.seniormbp.com/SeniorApps/facelets/registration/loginCenter.xhtml''', data=payload)
        except ConnectionError:
            raise MyBackpackBrokeError()

        if 'User Name or Password is not found' in r.text:
            raise AuthError
        try:
            self.session.get('https://thenewschool.seniormbp.com/SeniorApps/studentParent/academic/dailyAssignments/gradeBookGrades.faces')
            payload = {
                'f': 'f', 'f:_idcl': 'f:inside:j_id_jsp_1774471256_10pc5',
                'f:inside:UpcomingTab:AssignMPSel': '~~all~~',
                'javax.faces.ViewState':'j_id2'
            }
            r = self.session.post("https://thenewschool.seniormbp.com/SeniorApps/studentParent/academic/dailyAssignments/gradeBookGrades.faces",
                             data=payload)
        except ConnectionError:
            raise MyBackpackBrokeError()
        return r.text