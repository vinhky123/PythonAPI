import requests
import pandas as pd
import re
import numpy as np

def rating_crawl(rating_json):
    rating_dict = {
        'rating_star': rating_json['rating_star'],
        'comment': rating_json['comment']
    }
    return rating_dict

def extract_ids_from_shopee_url(url):
    item_id_pattern = r'i\.(\d+)\.(\d+)'
    shop_id_pattern = r'i\.(\d+)\.(\d+)'

    item_id_match = re.search(item_id_pattern, url)
    if item_id_match:
        item_id = item_id_match.group(2)
    else:
        item_id = None

    shop_id_match = re.search(shop_id_pattern, url)
    if shop_id_match:
        shop_id = shop_id_match.group(1)
    else:
        shop_id = None

    return item_id, shop_id

def rating_crawl(rating_json):
    rating_dict = {
        'rating_star': rating_json['rating_star'],
        'comment': rating_json['comment'],
    }
    return rating_dict

def crawl_shopee_comments(url_product):
    url = "https://shopee.vn/api/v2/item/get_ratings"
    limit = 6
    result = []

    item_id, shop_id = extract_ids_from_shopee_url(url_product)
    offset = 0
    while True:
        params = {
        "exclude_filter": 1,
        "filter": 0,
        "filter_size": 0,
        "flag": 1,
        "fold_filter": 0,
        "itemid": item_id,
        "limit": limit,
        "offset": offset,
        "relevant_reviews": False,
        "request_source": 2,
        "shopid": shop_id,
        "type": 0,
        "variation_filters": ""
    }
        headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Content-Type": "application/json",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Api-Source": "pc",
        "X-Csrftoken": "ZRzqGjOXobneugVAoFYr3z0d2jKskGvv",
        "X-Requested-With": "XMLHttpRequest",
    }
        response = requests.get(url, params=params,headers=headers)
        df = response.json()
        if df.get("data"):
            ratings = df["data"]["ratings"]   
        if not ratings:
            break
        for rating in ratings:
            rating_dict = rating_crawl(rating)
            result.append(rating_dict)
        offset += limit

    data = [result[i]['comment'] for i in range(len(result))]
    data = pd.DataFrame(data, columns=['comment'])
    number = len(data)
    data = data.loc[data['comment'] != '']
    return data, number