'''A badly written, example CRM app.'''
import itertools
import os
import sys
from typing import Dict, List, Optional

from sklearn import linear_model
from sklearn.model_selection import train_test_split

def check_domain(x):
    if 'gmail' in x:
        print('Importing gmail')
    elif 'hotmail' in x:
        print('Importing hotmail')
    else:
        print('Custom mail server.')

def input_info(lead):
    split_lead = lead.split()
    first_name = split_lead[0].replace(' ', '')
    last_name = split_lead[1]
    email = split_lead[2].lower()
    company = split_lead[3]
    twitter = split_lead[4].replace('@', '')
    website = split_lead[5].replace('https://', '')
    check_domain(email)
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'company': company,
        'twitter': twitter,
        'website': website,
    }

# split this up in 3.1
def import_leads(leads_file:str) -> List[Dict[str, str]]:  # function that is too long
    '''Import file, process leads, enrich leads, return processed_leads'''
    processed_leads = []

    try:
        with open(leads_file, 'rb') as f:
            leads = f.readlines()
            processed_leads = [input_info(lead) for lead in leads]

    except OSError:
        print('Cannot open file')

    return processed_leads


class Lead:

    def __init__(self,
                 company_website,
                 company_siz,
                 touchpoints = [],
                 days_since_last_post = 0,
                 discount = 1):
        self.company_website = company_website
        self.company_size = company_siz
        self.touchpoints = touchpoints
        self.days_since_last_post = days_since_last_post
        self.discount = discount

    @property
    def get_lead_score(self) -> int:
        return 1 if self.is_active() else 0

    @property
    def is_active(self) -> bool:
        return self.days_since_last_post < 5

    def get_lifetime_value(self, product) -> float:
        mrr = product.base_price() * self.discount
        return mrr * 12

    @property
    def priority(self) -> int:
        is_right_size = (self.company_size > 100) and (self.company_size < 100000)
        is_dotcom = self.company_website.endswith('.com')
        is_new_lead = len(self.touchpoints) == 0
        if is_right_size and is_dotcom and is_new_lead:
            return 100
        else:
            return 0

    def respose_action(self, services='', prompt:str ='') -> None:
        client = services.email.client('transactional', region='eu-ireland')
        response = client.send_email(
            destination= self.email,
            message={
                'body': {'Text': {prompt}},
                'subject': {'Text': {'Buy our stuff!'}}
            },
            source='refactoring@course.com'
        )
        print(response)

    def convert_lead(self, sevices):
        if self.company_size == 'smb':
            prompt = 'Hello small business!'
            self.respose_action(self, services, prompt)
        elif self.company_size == 'mid_market':
            prompt = 'Hello medium sized business!'
            self.respose_action(self, services, prompt)
        elif self.company_size == 'enterprise':
            prompt = 'Go say hello to this business!'
            self.respose_action(self, services, prompt)
        else:
            print('Wrong lead company type!')


class Customer(Lead):

    def __init__(self, company_website, company_size):
        super().__init__(company_website, company_size)

class CRMImportEntry:
    '''Entry imported from our legacy CRM.
    imported_data = {
        'name': {
            'first': 'John',
            'last': 'Smith'
        },
        'company': 'ACME',
        'deals': [13435, 33456]
    }
    '''

    @staticmethod
    def get_name_from_import(data: Dict) -> Dict:
        if 'name' in data:
            return data['name']
        else:
            print('Name not found.')
            return dict(first='', last='')

    def __init__(self, imported_data: Dict) -> None:
        inputs = CRMImportEntry.get_name_from_import(imported_data)
        self.first_name = inputs.get('first', '')
        self.last_name = inputs.get('last', '')
        self.num_deals = len(inputs.get('deals', []))






