import requests
class Scraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def scrape(self):
        r = self.session.get('''https://thenewschool.seniormbp.com/SeniorApps/facelets/registration/loginCenter.xhtml?convid=82232''')
        jsessionid = r.cookies['JSESSIONID']
        header = {
            'cookie': "JSESSIONID={}".format(jsessionid),
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        payload = {'form:signIn':'form:signIn', 'form:userId':self.username, 'form:userPassword': self.password,
                   'AJAXREQUEST':'_viewRoot', 'AJAX:EVENTS_COUNT': '1', 'form':'form', 'javax.faces.ViewState': 'j_id1'}

        self.session.post('''https://thenewschool.seniormbp.com/SeniorApps/facelets/registration/loginCenter.xhtml''', data=payload,
                         headers=header)
        header = {
            'cookie': "cookies=true; JSESSIONID={}".format(jsessionid),
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        r = self.session.get("https://thenewschool.seniormbp.com/SeniorApps/studentParent/academic/dailyAssignments/gradeBookGrades.faces", headers=header)
        return r.text