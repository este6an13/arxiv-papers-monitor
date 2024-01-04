import arxiv
import time

def get_previous_id():
    with open('id.txt') as f:
        PREVIOUS_ID = f.readline()
    id = int(PREVIOUS_ID.split('.')[1])
    return id

def write_last_id(id):
    with open('id.txt', 'w') as f:
        f.write(id)

def search_by_id(id):
    search = arxiv.Search(id_list = [id])
    results = list(search.results())
    if len(results) > 0:
        return results[0]
    return None

# not used yet
def get_month_id():
    from datetime import datetime  
    today = datetime.today()
    year = today.strftime("%y")
    month = today.strftime("%m")
    month_id = year + month
    return month_id

'''
KEYWORDS = [
            'explaina',
            'network',
            'priva',
            'comput',
            'graph',
            'physics',
            'algorithm',
            'language',
            'topo',
            'agent',
            'reservoir',
            'informed',
            'kernel',
            'search',
            'ensemble',
            'simulat',
            'attack',
            'knowledge',
            'decidab',
            'heterogen',
            'emergen',
            'complex',
            'bio',
            'hallucinat',
            'healthcare',
            'discover',
            'ontolog',
            'align',
            'interpret',
            'quan'
            ]
'''
CATEGORIES = ['cs.AI', 'cs.CC', 'cs.CL', 'cs.CR', 'cs.FL', 'cs.LG', 'cs.MA', 'cs.NE', 'cs.PL', 'cs.SI']

KEYWORDS = ['review', 'survey', 'art', 'overview']

# month_id = get_month_id()
month_id = 2401
id = get_previous_id()

while True:
    zpid = str(id).zfill(5) # zero padded id
    ID = f'{month_id}.{zpid}'
    try:
        result = search_by_id(ID)
        write_last_id(ID)
        if result == None:
            break
        '''
        # if category and (two or more keywords or review/survey)
        if any([cat in result.categories for cat in CATEGORIES]) and \
        ([kw in result.title.lower() for kw in KEYWORDS].count(True) > 1 or \
         any(kw in result.title.lower() for kw in ['review', 'survey'])):
        '''
        if any([cat in result.categories for cat in CATEGORIES]) and \
           any(kw in result.title.lower() for kw in ['review', 'survey']):
            #print(result.summary)
            print(result.title)
            print(result.pdf_url)
            print(result.categories)
            print()
        id += 1
    except Exception as e:
        print(e)
        time.sleep(60)
        continue
