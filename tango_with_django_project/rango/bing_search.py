import sys
import json
import urllib.request, urllib.parse, urllib.response, urllib.error
import requests
import pprint as pp


def read_bing_key():
    bing_api_key = None

    try:
        with open('bing.key','r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.key file not found')

    return bing_api_key


def run_query(search_terms):
    """
    :param search_terms: String containing search query
    :return: list of results from Bing search engine
    """
    query = join_args(search_terms)
    bing_api_key = read_bing_key()

    if not bing_api_key:
        raise KeyError("Bing Key Not Found")

    url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'

    payload = {'q': query,
               'responseFilter': 'webpages'}
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}

    results = []

    try:
        r = requests.get(url, params=payload, headers=headers)
        json_request = r.json()

        for page in json_request['webPages']['value']:
            results.append({
                'title': page['name'],
                'link': page['displayUrl'],
                'summary': page['snippet'],
            })

        return results

    except:
        print('error querying Bing API')


def join_args(*args):
    return " ".join([str(arg) for arg in args])


if __name__ == "__main__":
    query = join_args(sys.argv[1:])
    run_query(query)
