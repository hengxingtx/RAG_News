#! python3
# -*- encoding: utf-8 -*-
###############################################################
#          @Time    :   2025/07/09 18:57:13
#          @Author  :   heng
#          @Contact :   hengsblog@163.com
###############################################################
"""
@comment: 测试爬虫
"""
import requests
import urllib.parse

class GNewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://gnews.io/api/v4"
    
    def get_top_headlines(self, category='general', country='cn', lang='zh'):
        params = {
            'token': self.api_key,
            'category': category,
            'country': country,
            'lang': lang,
            'max': 10
        }
        
        response = requests.get(f"{self.base_url}/top-headlines", params=params)
        return response.json()
    
    def search_news(self, query, from_date=None, to_date=None):
        # 对查询字符串进行URL编码
        encoded_query = urllib.parse.quote(query)
        
        params = {
            'token': self.api_key,
            'q': encoded_query,
            'from': from_date,
            'to': to_date,
            'max': 10,
            'sortby': 'publishedAt'
        }
        
        response = requests.get(f"{self.base_url}/search", params=params)
        return response.json()
    

if __name__ == "__main__":
    api_key = "77ccf25a0666948435d80992a3f6d02c"
    gnews_api = GNewsAPI(api_key)
    # print(gnews_api.get_top_headlines())
    # 使用引号将短语括起来，确保作为一个整体搜索
    # print(gnews_api.search_news('"Hello"'))

    import requests

    url = 'https://gnews.io/api/v4/search'

    params = {
        'q': '中欧峰会',
        'lang': 'zh',
        'max': 5,
        'token': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    for article in data['articles']:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Published At: {article['publishedAt']}")
        print("---")