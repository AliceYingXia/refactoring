'''A badly written, example CRM app.'''
from dataclasses import dataclass, field
from typing import Dict, List, Optional

def check_domain(email: str) -> None:
    if 'gmail' in email:
        print('Importing gmail')
    elif 'hotmail' in email:
        print('Importing hotmail')
    else:
        print('Custom mail server.')

def input_info(info: str) -> Dict[str, str]:
    info = info.strip().split()
    first_name = info[0].replace(' ', '')
    last_name = info[1]
    email = info[2].lower()
    company = info[3]
    twitter = info[4].replace('@', '')
    website = info[5].replace('https://', '')
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
        with open(leads_file, "r", encoding="utf-8") as f:
            leads = f.readlines()
            processed_leads = [input_info(lead) for lead in leads]

    except OSError:
        print('Cannot open file')

    return processed_leads

@dataclass
class Lead:

        company_website: str
        company_size: int
        touchpoints = field(default_factory= list)
        days_since_last_post: int
        discount: float
        email: str

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

    def response_action(self, services='', prompt:str ='') -> None:
        client = services.email.client('transactional', region='eu-ireland')
        response = client.send_email(
            destination= self.email,
            message={
                'body': {'Text': prompt},
                'subject': {'Text': {'Buy our stuff!'}}
            },
            source='refactoring@course.com'
        )
        print(response)

    def convert_lead(self, services):
        if self.company_size == 'smb':
            prompt = 'Hello small business!'
            self.response_action(services, prompt)
        elif self.company_size == 'mid_market':
            prompt = 'Hello medium sized business!'
            self.response_action(services, prompt)
        elif self.company_size == 'enterprise':
            prompt = 'Go say hello to this business!'
            self.response_action(services, prompt)
        else:
            print('Wrong lead company type!')


@dataclass
class Customer(Lead):
    @classmethod
    def from_lead(cls, lead: Lead) -> "Customer":
        return cls(
            company_website=lead.company_website,
            company_size=lead.company_size,
            email=lead.email,
            days_since_last_post=lead.days_since_last_post,
            touchpoints=list(lead.touchpoints),
            discount=lead.discount,
        )

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