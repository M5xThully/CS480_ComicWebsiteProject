import json
import urllib


def read_bing_key():
    """
    this function reads the api key from a file called 'bing.key'
    returns: a string which will either return key found or key
    """
    bing_api_key = None

    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.key file not found')

    return bing_api_key


def run_query(search_terms):
    """
    this function returns a list of results from the Bing search engine
    """
    bing_api_key = read_bing_key()

    if not bing_api_key:
        raise KeyError("Bing Key Not Found")

    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    service = 'Web'
    results_per_page = 10
    offset = 0

    query = "'{0}'".format(search_terms)

    query = urllib.parse.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
            root_url,
            service,
            results_per_page,
            offset,
            query)

    username = ''

    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    password_mgr.add_password(None, search_url, username, bing_api_key)

    results = []

    try:
        # Prepare for connecting to Bing's servers.
        # Python 3 import (three lines)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)  # Py3
        opener = urllib.request.build_opener(handler)  # Py3
        urllib.request.install_opener(opener)  # Py3
        # Connect to the server and read the response generated.
        response = urllib.request.urlopen(search_url).read()  # Py3
        response = response.decode('utf-8')  # Py3

        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)

        # Loop through each page returned, populating out results list.
        for result in json_response['d']['results']:
            results.append({'title': result['Title'],
                            'link': result['Url'],
                            'summary': result['Description']})
    except:
        print("Error when querying the Bing API")

        # Return the list of results to the calling function.
    return results
