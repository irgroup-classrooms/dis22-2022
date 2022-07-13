from re import L
import pandas as pd
from rai_app import suggests
import os


def load_data(file):
    df = pd.read_excel(file)
    df['querrys'] = df['Vorname'] + ' ' + df['Name'] # create querry term column 
    return df

def get_user_input():
    input_source = input('Which search engine? Available selection: "google" or "bing"\n Input: ')
    input_max_depth = int(input('To what maximum depth should the search be carried out? Note: It is recommended to start with 1 \n Input: '))
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

    return user_input
  
def export_to_csv(df, path, sep=';'):
    df.to_csv(path, sep)

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

    # Export
    df.to_csv(export_path+'export.csv', sep=';', encoding='utf-8-sig')
    df.to_pickle(export_path+'export.pickle')
    df.to_json(export_path+'export.json')
 

if __name__ == "__main__":
    print(os.getcwd())
    main()
