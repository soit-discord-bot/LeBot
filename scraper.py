from bs4 import BeautifulSoup
import json
import requests

class Scraper:

    def __init__(self, year, unit):
        self.year = year
        self.unit = unit.upper()
        self.data = self.getdata()

    def getdata(self):
        url = f'https://handbook.monash.edu/api/content/render/false/query/+contentType:monash2_psubject%20+monash2_psubject.implementationYear:{self.year}%20+monash2_psubject.code:{self.unit}%20+conHost:4ebb02f6-d43f-45a8-90d2-8f7e1caa271b%20+deleted:false%20+working:true%20+live:true%20+languageId:1%20/orderBy/modDate%20desc%0A'
        html = requests.get(url)
        data = json.loads(html.content)
        try:
            data = json.loads(data['contentlets'][-1]['data'])
        except IndexError:
            print("No Unit Found")
        # print(data)
        return data

    def getunitcode(self):
        '''
        Retrieves the unit code from the data object.
        '''
        return self.data['unit_code'].strip()

    def getchiefexaminers(self):
        try:
            ces = list(filter(
                lambda obj: obj['role'] == 'Chief Examiner(s)', 
                self.data['academic_contact_roles']
            ))
        except KeyError:
            return []
        assert len(ces) == 1, 'Multiple Chief Examiner fields found!'
        ces = [obj['contact_title'].strip() + ' ' + obj['contact_name'].strip() for obj in ces[0]['contacts']]
        return ces

    def getassessments(self):
        categories = [assessment['assessment_name'].strip() for assessment in self.data['assessments']]
        weights = [assessment['weight'].strip() for assessment in self.data['assessments']]

        # if len(categories) == 0 and len(weights) == 0:
        #     soup = BeautifulSoup(self.data['handbook_assessment_summary'], 'html.parser')
        #     print(soup)

        return categories, weights


    