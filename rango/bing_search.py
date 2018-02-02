import json
import urllib

def read_bing_key():
    """
    Reads the BING API key from 'bing.key'.
    Returns a string witch is None or with a key.
    Remember: put bing.key in .gitignore to avoid committing it!
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
    Given a string containing search items (query),
    Returns a list of results from the Bing search engine.
    """
    bing_api_key = read_bing_key()

    if not bing_api_key:
        raise KeyError('Bing Key Not Found')

    # Specify the base url and the service
    # root_url = "https://api.datamarket.azure.com/Bing/Search/"
    root_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    service = 'Web'

    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page =10  and offset = 11, this would start from page 2.
    results_per_page =10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query will return then use is stored within variable query.
    query = "'{0}'".format(search_terms)

    # Turn the query into an HTML encoded string, using urllib.
    query = urllib.parse.quote(query)

    # Construct the later part of our request's URL.
    # Sets the format of our response to JSON and sets other properties.
    search_url = "{0}{1}?format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        service,
        results_per_page,
        offset,
        query)

    # Setup authentication with Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''

    # Setup a password manager to help authenticate our request.
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bing_api_key)

    # Create our results list which we'll populate.
    results =[]

    try:
        # Prepare for connecting to Bing's servers.
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

        # Connect to the server and read the response generated.
        response = urllib.request.urlopen(search_url).read()
        response = response.decode('utf-8')

        # Convert the string response to a python dictionary object.
        json_response = json.load(response)

        # Loop through each page returned, populating out results list.
        for result in json_response['d']['results']:
            results.append({'title': result['Title'],
                            'link': result['Url'],
                            'summary': result['Description']})
    except:
        print("Error when querying the Bing API")

    # Return the list of results to the calling function.
    return results


def main():
    test = input('Search: ')
    print(run_query(test))


if __name__ == '__main__':
    main()
