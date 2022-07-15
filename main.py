from re import L
import pandas as pd
from rai_app import suggests
import os
from functools import lru_cache


def load_data(file):
    df = pd.read_excel(file)
    df['querrys'] = df['Vorname'] + ' ' + df['Name'] # create querry term column 
    return df

def get_user_input():
    input_source = input('Which search engine? Available selection: "google" or "bing"\n Input: ')
    input_max_depth = int(input('To what maximum depth should the search be carried out? Note: It is recommended to start with 1 \n Input: '))
    option='option'
    
    while (option!='n') & (option!='y'):
        option = input('Do you want to use a Proxy Server? [y/n] \n Input: ')
        if option == 'n':
            user_input = {  'source': input_source,
                        'max_depth': input_max_depth,
                        'proxy_username': None,
                        'proxy_password': None,
                        'proxy_host': None,
                        'proxy_port': None
                        }
        elif option == 'y':
            proxy_username = input('Username: ')
            proxy_password = input('Password: ')
            proxy_host = input('Host: ')
            proxy_port = input('Port: ')


            user_input = {  'source': input_source,
                        'max_depth': input_max_depth,
                        'proxy_username': proxy_username,
                        'proxy_password': proxy_password,
                        'proxy_host': proxy_host,
                        'proxy_port': proxy_port
                        }
        else:
            print('try again)    

    return user_input
  
def export_to_csv(df, path, sep=';'):
    df.to_csv(path, sep)

def lev_dist(a, b):
    '''
    This function will calculate the levenshtein distance between two input
    strings a and b
    
    params:
        a (String) : The first string you want to compare
        b (String) : The second string you want to compare
        
    returns:
        This function will return the distnace between string a and b.
        
    example:
        a = 'stamp'
        b = 'stomp'
        lev_dist(a,b)
        >> 1.0
    '''
    
    @lru_cache(None)  # for memorization
    def min_dist(s1, s2):

        if s1 == len(a) or s2 == len(b):
            return len(a) - s1 + len(b) - s2

        # no change required
        if a[s1] == b[s2]:
            return min_dist(s1 + 1, s2 + 1)

        return 1 + min(
            min_dist(s1, s2 + 1),      # insert character
            min_dist(s1 + 1, s2),      # delete character
            min_dist(s1 + 1, s2 + 1),  # replace character
        )

    return min_dist(0, 0)

#source: https://towardsdatascience.com/text-similarity-w-levenshtein-distance-in-python-2f7478986e75

def lev_dist_row(row):
    scores = []
    for root_word in row.root.split():
        for target_word in row.target.split():
            scores.append(lev_dist(root_word, target_word))
    if any(score<3 for score in scores):
        return row.target
    else:
        return 'delete'

def main():
    import_path = 'rai_app/import_file/import.xlsx'
    export_path = 'rai_app/export_file/'

    file = load_data(import_path)
    df = pd.DataFrame()

    user_input = get_user_input()
    # Crawl querrys and safe output 
    for querry in file['querrys']:
        # Generating a suggestions tree
        tree = suggests.get_suggests_tree(
            querry.lower(), 
            source=user_input['source'], 
            max_depth=user_input['max_depth'],
            proxy_username=user_input['proxy_username'],
            proxy_password=user_input['proxy_password'],
            proxy_host=user_input['proxy_host'],
            proxy_port=user_input['proxy_port']
            )

        
        # Reduce to new information obtained in suggestions
        edges = suggests.to_edgelist(tree)
        edges = suggests.add_parent_nodes(edges)
        try:
            edges = edges.apply(suggests.add_metanodes, axis=1)
            # Append output to df
            df = pd.concat([df,edges])
        except AttributeError:
            pass

    df['target'] = df.apply(lev_dist_row, axis=1)
    df = df.loc[df.target!='delete']
    

    # Export
    df = df.reset_index(drop=True)
    df.to_csv(export_path+'export.csv', sep=';', encoding='utf-8-sig')
    df.to_pickle(export_path+'export.pickle')
    df.to_json(export_path+'export.json')
 

if __name__ == "__main__":
    print(os.getcwd())
    main()
