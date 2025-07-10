import newspaper
from newspaper import news_pool

class FreeNewsCrawler:
    def __init__(self):
        self.news_sources = [
            'http://cnn.com',
            'http://bbc.co.uk',
            'http://reuters.com',
            'http://apnews.com'
        ]
    
    def parallel_scrape(self):
        papers = [newspaper.build(url) for url in self.news_sources]
        news_pool.set(papers, threads_per_source=2)
        news_pool.join()
        
        all_articles = []
        for paper in papers:
            for article in paper.articles:
                try:
                    article.download()
                    article.parse()
                    all_articles.append({
                        'title': article.title,
                        'text': article.text,
                        'url': article.url,
                        'publish_date': article.publish_date,
                        'source': paper.brand
                    })
                except:
                    continue
        
        return all_articles
    

if __name__ == "__main__":
    crawler = FreeNewsCrawler()
    articles = crawler.parallel_scrape()
    print(articles)