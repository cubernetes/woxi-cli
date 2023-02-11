#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import json

def main(query='hallo'):
    template_url = 'https://synonyme.woxikon.de/synonyme/%s.php'
    url = template_url % query
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')

    os.system('')

    def formatMeaning(text):
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.replace(' Bedeutung', '. Bedeutung')
        return text

    card_list = []
    for card in soup.select('li.synonyms-list-item.clear-content:not(.text-center)'):
        synonym_group = card.select_one('div.synonyms-list-header').text
        synonym_group = formatMeaning(synonym_group)
        upper_synonyms = card.select_one('div.upper-synonyms')
        lower_synonyms = card.select_one('div.lower-synonyms')
        card_list.append({
            'synonymGroup': synonym_group,
            'upperSynonyms': [],
            'lowerSynonyms': []
        })
        
        if upper_synonyms is not None:
            for syn in upper_synonyms.find_all('a'):
                syn = syn.text
                card_list[-1]['upperSynonyms'].append(syn)

        if lower_synonyms is not None:
            for syn in lower_synonyms.find_all('a'):
                syn = syn.text
                card_list[-1]['lowerSynonyms'].append(syn)

    card_list = card_list[::-1]
    out = json.dumps(card_list, indent=2, ensure_ascii=False)
    print(out)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        main("%20".join(sys.argv[1:]))
