import argparse
import urllib.parse
import pandas as pd
from pathlib import Path

def addToCSV(name: str, url: str, path: str):
    '''If the given item exists in the CSV file, it updates the link
       if it doesn't exist, it appends the item at the end of the file    
    '''
    if(not Path(path).exists()):
        df = pd.DataFrame({'Item Name':[],'Steam Link':[]})
    else:
        df = pd.read_csv(path)
    if name in df['Item Name'].values:
        df.loc[df['Item Name'] == name, 'Steam Link'] = url
    else:
        new_row = {'Item Name': name, 'Steam Link': url}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(path, index=False)

def parseLink(url: str):
    '''Parses the steam marketplace link to extract app id and item name'''
    split_url = url.split('/')
    appid = split_url[5]
    raw_name = split_url[6]
    return appid, raw_name
def main():

    parser = argparse.ArgumentParser(description="Generates json links for the price history of cs2 items")
    parser.add_argument("--url",type=str, help="Url of the marketplace listing")
    parser.add_argument("--path",type=str,default="../data/steamlinks.csv",help="CSV path for steam links.")
    args = parser.parse_args()

    appid, raw_name = parseLink(args.url)

    link = f"https://steamcommunity.com/market/pricehistory/?appid={appid}&market_hash_name={raw_name}"

    # Decodes url encoded string into normal string
    clean_name = urllib.parse.unquote(raw_name)

    addToCSV(clean_name,link,args.path)

if __name__ == "__main__":
    main()