# 爬取人民日报热榜

import requests
from xml.etree import ElementTree


def get_ranking():
    # 使用中新网的RSS源作为替代
    url = "http://www.chinanews.com.cn/rss/scroll-news.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        # 检查请求是否成功
        response.raise_for_status()

        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP错误: {http_err}"
    except requests.exceptions.RequestException as err:
        return f"请求发生错误: {err}"


# 获取XML文本
xml_text = get_ranking()

# 解析并打印新闻标题
if not xml_text.startswith("HTTP错误") and not xml_text.startswith("请求发生错误"):
    try:
        root = ElementTree.fromstring(xml_text)
        print("中新网即时新闻标题：")
        # RSS item通常在 channel -> item 路径下
        for item in root.findall("./channel/item"):
            title = item.find("title").text
            print(f"- {title}")
    except ElementTree.ParseError as e:
        print(f"解析XML失败: {e}")
        print("收到的内容可能不是有效的XML格式：")
        print(xml_text)
else:
    print(xml_text)
