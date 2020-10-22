from bs4 import BeautifulSoup
# from lxml import html
import requests
from re import sub

# import json
# a = [[1, 2], [3, 4]]
# print(json.dumps(a))
# a = json.dumps(a)
# print(type(a))
# print(json.loads(a)[0])

pre_link = 'http://slounik.org/search?'
# // mode = 0
belru_dicts = ['nb', 'bulykarb', 'krapivarb', 'vlastrb', 'sanko', 'rbSauka', 'lingrb', 'miedrb', 'fizyjarb',
               'farmarb', 'bijarb', 'lashasrb', 'ekanamrb', 'ekanam2rb', 'fizmat', 'matrb', 'cyhunrb', 'vajskovy',
               'bn', 'bulykabr', 'stanbr', 'krapivabr', 'biez', 'miedbr', 'vierasbr', 'polisemija']
# // mode = 1
explain_dicts = ['tlum', 'tsbm', 'slovaklad', 'prynaz', 'fraza', 'starbiel', 'hsbm', 'calaviek', 'zyvioly',
                 'rasliny', 'sielhas', 'dyjalekt', 'krajovy', 'viciebscyna', 'vusaccyna', 'lahojsk',
                 'paraunanni', 'roznajes', 'bnt01', 'bnt02', 'bnt03', 'bnt04', 'bnt05', 'bnt06a', 'bnt06b',
                 'bnt07', 'bnt08', 'bnt09', 'bnt10', 'bnt11', 'bnt12', 'bnt13', 'bnt14', 'bnt15', 'bnt16',
                 'bnt17', 'bnt18', 'bnt19', 'bnt20', 'bnt21', 'bnt23', 'bnt24', 'bnt25', 'bnt26', 'bnt27',
                 'bnt28', 'bnt29']
# // mode = 2
lexical_dicts = ['sbm', 'nazounik', 'dzsl', 'prym', 'paronimy', 'epitety', 'sinonimyk', 'bkp2005']
# // mode = 3
encyclopedia = ['pismienniki', 'reldz', 'ruchi', 'demap', 'nac', 'asvietniki', 'kulturalogia', 'mify',
                'architekt', 'cerkvy', 'matematyka', 'hramadstva', 'sac', 'czyrvon', 'amfibii', 'eka',
                'mikrabija', 'virus', 'gieagraf', 'gieabiel', 'ist', 'kto', 'filmyr', 'historical',
                'statehood', 'schrift']

dict_organizer =[belru_dicts, explain_dicts, lexical_dicts, encyclopedia]

def generate_link(search, dict=[0], un=1):
    dict_list = ''
    for i in range(len(dict)):
        dict_list += '|'.join(dict_organizer[i]) * dict[i]
    post_link = 'search=' + search + '&dict=' + dict_list + '&un=' + str(un)
    # final = urllib.parse.quote(link, safe='')
    final = pre_link + post_link
    print('usage: ', dict_list)
    print('- - - -- link:  ', final)
    return final

def get_translations(word, dict=[0], un=1):
    # print(dict)
    final_link = generate_link(word, dict=dict, un=un)
    response = requests.get(final_link)

    # dictionaries_html = open('encyclopedia.html', 'r+')
    ## soup_object = BeautifulSoup(response.text, 'lxml')
    ## soup_object = soup_object.find_all('a', class_='li')
    ## soup_object = soup_object.find('li')
    # encyclopedia = []
    # soup_object = BeautifulSoup(dictionaries_html, 'lxml')
    # translate_dictionaries = soup_object.find_all('input', checked='on')
    # for each in translate_dictionaries:
    #     if 'name' in each.attrs:
    #         encyclopedia.append(each.attrs['name'])
    # print(encyclopedia)

    soup_object = BeautifulSoup(response.text, 'lxml')
    # w = open('web.html', 'w')
    # w.write(response.text)
    # w.close()
    list_of_translations = []
    translations = soup_object.find_all('li', id='li_poszuk')
    # print(len(translations))
    # print(*translations, sep='\n'+'_'*20+'\n')
    for each in translations:
        # each = str(each).replace('"', "''")
        without_comments = sub('(<!--.*?-->)', '', str(each))
        res = without_comments.split('// ')
        result = res[0].replace('\t', '    ')
        source = BeautifulSoup(res[1], 'lxml')
        # print(' --- -- - - - ', source)
        dict_name = source.html.body.a.attrs['title']
        dict_link = 'http://slounik.org' + source.html.body.a.attrs['href']
        source = '<a href="%s">%s</a>' % (dict_link, dict_name)
        # print(soup2.prettify())
        result = result.replace('<li id="li_poszuk">', '')
        result = result.replace('<br/>', '\t')
        list_of_translations.append([result, source])

    # print(len(list_of_translations))
    return list_of_translations
    # list of lists kinda[translation | book, it was taken from]

if __name__ == '__main__':
    print(*get_translations('марка', dict=[2]), sep='\n')