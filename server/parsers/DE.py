import arrow
import json, re
import requests

COUNTRY_CODE = 'DE'

def fetch_DE():
    r = requests.session()
    formatted_date = arrow.now(tz='Europe/Berlin').format('DD.MM.YYYY')
    url = 'https://www.agora-energiewende.de/en/topics/?type=371842&tx_agoragraphs_agoragraphs%5Breferer%5D=https%3A%2F%2Fwww.agora-energiewende.de%2Fen%2Ftopics%2F-agothem-%2FProdukt%2Fprodukt%2F76%2FAgorameter%2F&tx_agoragraphs_agoragraphs%5Baction%5D=renderPowerGeneration&tx_agoragraphs_agoragraphs%5Bcontroller%5D=Graph&tx_agoragraphs_agoragraphs%5BstartDate%5D={}&tx_agoragraphs_agoragraphs%5BendDate%5D={}'.format(formatted_date, formatted_date)
    response = r.get(url)
    body = response.text

    parsed = {}
    for s in re.findall('{"id":"(.*?)",.*?,"data":(.*?)(,"|})', body):
        parsed[s[0]] = json.loads(s[1])[-1]

    data = {
        'countryCode': COUNTRY_CODE,
        'datetime': arrow.get(arrow.get(parsed['wind'][0] / 1000.0).datetime, 
            'Europe/Berlin').datetime,
        'production': {
            'wind': parsed['wind'][1],
            'solar': parsed['solar'][1],
            'biomass': parsed['biomass'][1],
        },
        'consumption': {
            'other': parsed['total-load'][1]
        }
    }
    
    return data

fetch_DE()
