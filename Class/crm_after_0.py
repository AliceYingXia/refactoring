'''A badly written, example CRM app.'''

def check_domain(x):
    if 'gmail' in x:
        print('Importing gmail')
    elif 'hotmail' in x:
        print('Importing hotmail')
    else:
        print('Custom mail server.')

def input_info(lead):
    processed_lead = {}
    split_lead = lead.split()
    processed_lead['first_name'] = split_lead[0].replace(' ', '')
    processed_lead['last_name'] = split_lead[1]
    processed_lead['email'] = split_lead[2].lower()
    check_domain(processed_lead['email'])
    processed_lead['company'] = split_lead[3]
    processed_lead['twitter'] = split_lead[4].replace('@', '')
    processed_lead['website'] = split_lead[5].replace('https://', '')
    return processed_lead

# split this up in 3.1
def import_leads(leads_file):  # function that is too long
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
    def get_lead_score(self):
        return 1 if self.is_active() else 0

    @property
    def is_active(self):
        return self.days_since_last_post < 5

    @property# 3.2: mrr should be inlined to the return statement
    def get_lifetime_value(self, product):
        mrr = product.base_price() * self.discount
        return mrr * 12

    @property
    def priority(self):
        is_right_size = (self.company_size > 100) and (self.company_size < 100000)
        is_dotcom = self.company_website.endswith('.com')
        is_new_lead = len(self.touchpoints) == 0
        if is_right_size and is_dotcom and is_new_lead:
            return 100
        else:
            return 0

    def respose_action(self, services='', prompt):
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
    def get_name_from_import(data):
        if 'name' in data:
            return data['name']
        else:
            print('Name not found.')
            return dict(first='', last='')

    def __init__(self, imported_data):

        self.first_name = get_name_from_import(imported_data).get('first', '')
        self.last_name = get_name_from_import(imported_data).get('last', '')
        self.num_deals = len(imported_data.get('deals', []))






