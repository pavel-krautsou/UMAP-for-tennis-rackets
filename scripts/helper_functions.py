import requests
from bs4 import BeautifulSoup
import pandas as pd

def getSoup(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print(f'Unable to retrive source code for {url}')
        return None
def get_product_links_table(soup):
    products = soup.find_all(class_='cattable-wrap-cell-imgwrap-inner is-racquet')
    product_names = [product.find('img').attrs['alt'] for product in products]
    product_links = [product['href'] for product in products]
    d = {'names':product_names,  'links': product_links}
    return pd.DataFrame(d)


def getTable(soup):
    table = soup.find('tbody')
    rows = table.find_all('tr')
    # Initialize lists to store attributes and values
    attributes = []
    values = []
    # Iterate over each row and extract the attribute and value
    for row in rows:
        cols = row.find_all('td')
        attribute = cols[0].get_text(strip=True).replace(':', '')  # Clean up the attribute text
        value = cols[1].get_text(strip=True)
        # Append to the lists
        attributes.append(attribute)
        values.append(value)
    df = pd.DataFrame({
        'Attribute': attributes,
        'Value': values
    })
    return df


def getTable2(soup):
    table = soup.find('tbody')
    rows = table.find_all('tr')
    # Initialize lists to store attributes and values
    attributes = []
    values = []
    # Iterate over each row and extract the attribute and value
    for row in rows:
        print(f'Row:{row}')
        text = row.find('td')
        print(f'text:{text}')
        attribute = row.find('td').find('b').text
        value = row.find('td').find('strong').next_sibling.strip()
        # Append to the lists
        attributes.append(attribute)
        values.append(value)
    df = pd.DataFrame({
        'Attribute': attributes,
        'Value': values
    })
    return df







def formatTheTable(d):
    tmp = d.set_index('Attribute').T
    tmp.columns = tmp.columns.str.strip()
    translation = {'Schlagfläche': 'HeadSize',
                       'Länge': 'Length',
                       'Gewicht': 'StrungWeight',
                       'Gewicht (unbesaitet)': 'UnStrungWeight',
                       'Balance': 'Balance',
                       'Balance (unbesaitet)': 'UnstrungBalance',
                       'Schwunggewicht': 'SwingWeight',
                       'Rahmenhärte': 'Stiffness',
                       'Rahmenstärke': 'BeamWidth',
                       'Material': 'Composition',
                       'Schlägerfarbe': 'RacketColours',
                       'Griffband': 'GripType',
                       'Saitenmuster': 'StringPattern',
                       'Besaitungshärte': 'StringTension'}
    tmp = tmp[translation.keys()].rename(columns=translation)
    return tmp

def cleanTheTable(d):
    tmp = d.copy()
    tmp[['BeamWidth1', 'BeamWidth2', 'BeamWidth3']] = tmp['BeamWidth'].str.split(' / ', expand=True)
    tmp[['NumMains', 'NumCrosses']] = tmp['StringPattern'].str.split(' / ', expand=True)
    tmp[['MinStringTension', 'MaxStringTension']] = tmp['StringTension'].str.split('-', expand=True)
    cols = ['HeadSize', 'Length', 'StrungWeight', 'UnStrungWeight', 'SwingWeight',
            'Balance', 'Stiffness',
            'BeamWidth1', 'BeamWidth2', 'BeamWidth3',
            'NumMains', 'NumCrosses', 'MinStringTension', 'MaxStringTension'
            ]
    cols = [col for col in cols if col in tmp.columns]
    for col in cols:
        tmp[col] = tmp[col].str.replace(",", '.').str.extract(r'(\d+\.?\d*)').astype(float)
    tmp['StringDensity'] = tmp['HeadSize']/(tmp['NumMains']*tmp['NumCrosses'])
    return tmp[cols + ['StringDensity']]


def customFormat(val):
    if val % 1 == 0:  # If the value is an integer
        return f'{int(val)}'  # Display as integer
    else:
        return f'{val:.2f}'  # Display with one decimal place

