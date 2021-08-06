import json
import requests

def read_bing_key():
    # Reads the secret key. DM.
    bing_api_key = '5fa6f41e5fc743609221010e3986a724'

   
    
    return bing_api_key

def run_query(search_terms):
    bing_key = read_bing_key()
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    #endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/search"
    headers = {'Ocp-Apim-Subscription-Key': bing_key}
    params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    results = []
    for result in search_results['webPages']['value']:
        results.append({'title': result['name'], 'link': result['url'], 'summary': result['snippet']})
    
    return results

def main():
    # Alternative solution for terminal-based interaction. DM.
    search_terms = input("Enter your query terms: ")
    results = run_query(search_terms)

    for result in results:
        print(result['title'])
        print(result['link'])
        print(result['summary'])
        print('===============')

if __name__ == '__main__':
    main()