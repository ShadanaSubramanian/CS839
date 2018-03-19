import scrapy
class BestBuySpider(scrapy.Spider):
    name ="amazon"
    def start_requests(self):
        # urls =[
        #        "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=cat02012&st=cat02012_categoryid%24cat02001&qp=&sp=-bestsellingsort%20skuidsaas",
        #     "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=cat02012&st=cat02012_categoryid%24cat02001&qp=genre_facet%3DGenre~New%20Age&sp=-bestsellingsort%20skuidsaas",
        #     "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=cat02012&st=cat02012_categoryid%24cat02001&qp=genre_facet%3DGenre~New%20Age%5Egenre_facet%3DGenre~Rock&sp=-bestsellingsort%20skuidsaas"
        #        ]
        urls = ["https://www.amazon.com/s/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A5174%2Cn%3A37%2Ck%3Amusic&keywords=music&ie=UTF8&qid=1521421707",
                ]
        for url in urls:
            yield  scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = response.xpath('//*[@id="s-results-list-atf"]/li')
        for content in contents:
            sponsored = content.xpath('div/div/div/div[2]/h5')#to avoid sponsored contents from amazon
            if not sponsored:
                title = content.css('.s-access-title::text').extract_first()
                year = content.xpath('div/div/div/div[2]/div[1]/div[1]/span[3]/text()').extract_first()
                artist = content.xpath('div/div/div/div[2]/div[1]/div[2]/span[2]/a/text()').extract_first()
                price = content.css('span.a-size-base.a-color-price.s-price.a-text-bold::text').extract_first()#as css seems better than xpath for price
                yield {
                    'title': title,
                    'artist': artist,
                    'release': year,
                    'price': price,
                }
        links = response.xpath('//*[@id="pagn"]/span')
        for l in links:
            if l is not None:
                next_page = l.css('a::attr(href)').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(url=next_page, callback=self.parse)
