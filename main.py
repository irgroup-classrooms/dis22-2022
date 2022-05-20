from re import L
import pandas as pd
from rai_app import suggests

def load_data():
    file = 'querries.xlsx'
    df = pd.read_excel(file)
    df['querrys'] = df['Vorname'] + ' ' + df['Name'] # create querry term column 
    return df

def get_user_input():
    input_source = input('Which search engine? Available selection: "google" or "bing"\n Input: ')
    input_max_depth = int(input('To what maximum depth should the search be carried out? Note: It is recommended to start with 1 \n Input: '))
    user_input = {'source': input_source,
             'max_depth': input_max_depth}
    return user_input

def main():
    input = load_data()
    output = pd.DataFrame()
    user_input = get_user_input()

    # Crawl querrys and safe output 
    for querry in input['querrys']:
        # Generating a suggestions tree
        tree = suggests.get_suggests_tree(querry.lower(), source=user_input['source'], max_depth=user_input['max_depth'])
        
        # Reduce to new information obtained in suggestions
        edges = suggests.to_edgelist(tree)
        edges = suggests.add_parent_nodes(edges)
        edges = edges.apply(suggests.add_metanodes, axis=1)

        # Append output to df
        output = output.append(edges)

    output.to_csv('output.csv')

if __name__ == "__main__":
    main()