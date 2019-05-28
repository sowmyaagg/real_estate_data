import nltk
import slimit
import pandas as pd
import json
#nltk.download('popular')
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
import pprint
import re
#https://likegeeks.com/nlp-tutorial-using-python-nltk/
# https://pythonspot.com/category/nltk/
from itertools import chain, starmap


def convert_to_list(potential_scalar):
    if not isinstance(potential_scalar, list):
        potential_scalar = [potential_scalar]

    return potential_scalar

def flatten_json_iterative_solution(dictionary): #https://towardsdatascience.com/how-to-flatten-deeply-nested-json-objects-in-non-recursive-elegant-python-55f96533103d
    """Flatten a nested json file"""


    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!

        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = key #parent_key + '_' + key
                yield temp1, value

        elif isinstance(parent_value, list):
            i = 0
            for value in parent_value:
                temp2 = str(i) #parent_key + '_' + str(i)
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value

            # Keep iterating until the termination condition is satisfied

    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
                not any(isinstance(value, list) for value in dictionary.values()):
            break

    return dictionary


def get_dataframe_from_zillow_url(zillow_url):

    # method allowed for urllib.request.urlopen is GET, for that we need to pass a request object in place of url
    # the headers must be in dictionary format
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    headers    = {'User-Agent':user_agent}
    Request_Obj= urllib.request.Request(zillow_url,headers = {'User-Agent':user_agent})
    response   = urllib.request.urlopen(Request_Obj)   # https://docs.python.org/3/library/urllib.request.html#module-urllib.request

    html     = response.read()

    # method to parse a website with re: https://pythonprogramming.net/parse-website-using-regular-expressions-urllib/
    # method to parse with bs4: https://codeburst.io/web-scraping-101-with-python-beautiful-soup-bb617be1f486

    # for zillow specific listing parse at 1) 'WordmarkSaveShareMore  'us{"ForSaleDoubleScrollInitialRenderSEOQuery{\\"zpid\\":

    # Use the beautiful soup to parse the html, get the text

    soup     = BeautifulSoup(html,'html.parser')
    text     = soup.get_text(strip=True)
    text_raw = soup.contents
    #pprint.pprint(text_raw)


    # try to parse zillow specific page - just see the html
    #reg_ex_result = re.findall(r'WordmarkSaveShareMore(.*?)comp',text)
    data          = json.loads(soup.find('script', id='hdpApolloPreloadedData', type='application/json').text)
    #print(soup_main)
    print(type(data))


    Data = flatten_json_iterative_solution(data)
    #pprint.pprint(Data)

    Data = dict(zip(Data.keys(),[convert_to_list(val) for val in Data.values()])) #converting scalar values to list for dataframe conversion
    #pprint.pprint(Data)

    DataDf = pd.DataFrame.from_dict(Data)
    pprint.pprint(DataDf)

def rearrange_dataframe_cols(DataDf):
    DataDf = DataDf[['']]

def get_zillow_url_from_google(google_search_str):
    url = ''

url    = 'https://www.zillow.com/homedetails/1705-33rd-Ave-Seattle-WA-98122/49046624_zpid/'  # Zillow works:
# 'https://www.zillow.com/homes/for_sale/fsba,fsbo,new,cmsn_lt/house_type/b05ae5cc0cX1-CR1cn293ihpoy9q_1276cw_crid/1-_beds/0-1200000_price/0-4724_mp/1100-_size/built_sort/47.70826,-122.18668,47.587757,-122.470951_rect/X1-SS8vh6od7uleov1000000000_7q4ks_sse/0_mmm/' # Main zillow search works
# Redfin works: 'https://www.redfin.com/WA/Seattle/1705-33rd-Ave-98122/home/145993'
# Google works: 'https://www.google.com/search?q=1705+33rd+Ave%2C+98122&oq=1705+33rd+Ave%2C+98122&aqs=chrome..69i57j0.440j0j4&sourceid=chrome&ie=UTF-8'

DataDf = get_dataframe_from_zillow_url(url)

'''
    # Use iterables to get the tokens and nltk to eliminate the stop words
    tokens   = [token for token in text.split() if token not in stopwords.words('english')]
    
    
    # Use nltk to create a freq distribution of tokens
    freq     = nltk.FreqDist(tokens)
    freq.plot(40,cumulative=False) '''
