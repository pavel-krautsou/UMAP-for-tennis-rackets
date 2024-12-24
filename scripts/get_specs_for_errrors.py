import pandas as pd
import os
from helper_functions import formatTheTable, cleanTheTable, getTable2
import pickle as pkl

if __name__ == "__main__":
    with open(f"../data/error_lst.pkl", "rb") as file:
        error_lst = pkl.load( file)
    new_error_dict = dict()
    resultDF = pd.DataFrame()
    for error_path in error_lst:
        brand = error_path.split('/')[2]
        model = error_path.split('/')[3].replace('.pkl', '')
        try:
            with open(error_path, "rb") as file:
                soup = pkl.load(file)
            df = getTable2(soup)
            formated_df = formatTheTable(df)
            cleanDF = cleanTheTable(formated_df)
            cleanDF['Brand'] = brand
            cleanDF['Model'] = model
            resultDF = pd.concat([resultDF, cleanDF])
        except Exception as e:
            print(e)
            #print(f'error occured for {error_path}')
            new_error_dict[error_path] = e

    error_df = pd.DataFrame.from_dict(new_error_dict)
    error_df.to_csv('data/errors.csv', index=False)
    resultDF.to_csv('data/raquets_dataset2.csv', index=False)
    print(f'number of raquets missing:{len(new_error_list)}')




with open(f"../data/error_lst.pkl", "rb") as file:
    error_lst = pkl.load(file)
new_error_dict = dict()
resultDF = pd.DataFrame()
for error_path in error_lst:
    brand = error_path.split('/')[2]
    model = error_path.split('/')[3].replace('.pkl', '')
    try:
        with open(error_path, "rb") as file:
            soup = pkl.load(file)
        df = getTable2(soup)
        formated_df = formatTheTable(df)
        cleanDF = cleanTheTable(formated_df)
        cleanDF['Brand'] = brand
        cleanDF['Model'] = model
        resultDF = pd.concat([resultDF, cleanDF])
    except Exception as e:
        new_error_dict[error_path] = str(e)


df = pd.DataFrame({'paths':new_error_dict.keys(),
 'errors':new_error_dict.values()})


with open('../data/htmls/Wilson/WilsonBlade104v9.pkl', "rb") as file:
    soup = pkl.load(file)

rows = soup.find_all(class_="SpecsLt")


row = rows[0]
df.groupby('errors').size()