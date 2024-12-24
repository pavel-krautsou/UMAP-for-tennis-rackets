
import pickle as pkl
from helper_function import get_product_links_table, getSoup
# helper functions




# URL of the page to scrape

## Brands and links to
brands = ['Wilson', 'Babolat', 'Head', 'Yonex', 'Technifibre', 'Dunlop',
          'Volkl', 'ProKennex', 'Lacoste', 'Solinco', 'Prince']

posfixes = ['/catpage-WILSONRACS-DE.html', '/catpage-BABOLATRAC-DE.html',"/catpage-HEADRAC-DE.html",
            "/catpage-YONEXRAC-DE.html", "/catpage-TECRAC-DE.html", "/catpage-DUNLOPRAC-DE.html",
            "/catpage-VOLRAC-DE.html", "/catpage-PROKERAC-DE.html", "/catpage-LRAC-DE.html",
            "/catpage-SOLRAC-DE.html", '/catpage-PRINCERAC-DE.html'
            ]


base_url = 'https://www.tenniswarehouse-europe.com'




if __name__ == "__main__":
    for brand, postfix in zip(brands, posfixes):
        url = base_url + postfix
        soup = getSoup(url)
        with open(f"data/soups/{brand}.pkl", "rb") as file:
            soup = pkl.load(file)
        if soup is not None:
            links_table = get_product_links_table(soup)
            links_table['brand'] = brand
            links_table.to_csv(f'data/rackets_and_links/{brand}.csv')



