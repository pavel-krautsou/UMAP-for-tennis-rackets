from bs4 import BeautifulSoup
import pandas as pd
import os
from helper_functions import formatTheTable, cleanTheTable, getTable
import pickle as pkl


brands = ['Wilson', 'Babolat', 'Head', 'Yonex', 'Technifibre', 'Dunlop',
          'Volkl', 'ProKennex', 'Lacoste', 'Solinco', 'Prince']

resultDF = pd.DataFrame()
error_lst = []
if __name__ == "__main__":
    for brand in brands:
        base_path = f'UMAP-for-tennis-rackets/data/htmls/{brand}'
        file_lst = os.listdir(base_path)
        file_lst = [f for f in file_lst if 'Kinder' not in f]
        file_lst = [f for f in file_lst if 'Junior' not in f]
        for fp in file_lst:
            try:
                with open(f"UMAP-for-tennis-rackets/data/htmls/{brand}/{fp}", "rb") as file:
                    soup = pkl.load(file)
                df = getTable(soup)
                formated_df = formatTheTable(df)
                cleanDF = cleanTheTable(formated_df)
                cleanDF['Brand'] = brand
                cleanDF['Model'] = fp.replace('.pkl', '')
                resultDF = pd.concat([resultDF,cleanDF ])
            except:
                print(f'error occured for {fp}')
                error_lst.append(f"data/htmls/{brand}/{fp}")

    resultDF.to_csv('data/raquets_dataset2.csv', index=False)
    print(f'number of raquets missing:{len(error_lst)}')
    with open(f"../data/error_lst2.pkl", "wb") as file:
        pkl.dump(error_lst, file)


