import pandas as pd
import os
import pickle as pkl
import time
from helper_functions import getSoup


brands = ['Wilson', 'Babolat', 'Head', 'Yonex', 'Technifibre', 'Dunlop',
          'Volkl', 'ProKennex', 'Lacoste', 'Solinco', 'Prince']

if __name__ == "__main__":
    for brand in brands[1:2]:
        fp = f'data/raquets_and_links/{brand}.csv'
        df = pd.read_csv(fp)
        ## Create destination folder if it doesn't exist
        dest_fp = f'data/htmls/{brand}'
        if not os.path.exists(dest_fp):
            os.makedirs(dest_fp)
        ## clean the names column
        df['names'] = df['names'].str.replace('Tennissch.*', '', regex=True).str.strip()
        df['names'] = df['names'].str.replace('Schl.*', '', regex=True).str.strip()
        df['names'] = df['names'].str.replace(' ', '', regex=True)
        df['names'] = df['names'].str.replace('/', '', regex=False)
        for index, row in df.iterrows():
            time.sleep(6)
            soup = getSoup(row['links'])
            if soup is not None:
                with open(f"UMAP-for-tennis-rackets/data/htmls/{brand}/{row['names']}.pkl", "wb") as file:
                    pkl.dump(soup, file)
                print(f'Successfuly ran for {row["names"]}')





#row = {'names': df.iloc[0,1], 'links':df.iloc[0,2]}
#with open(f"data/soups/{brand}/{row['names']}.pkl", "wb") as file:
#    soup = pkl.load(file)