import scrapy
from collections import OrderedDict
class BestBuySpider(scrapy.Spider):
    name ="bestbuy"#name of the spider
    '''
        start method called by the Srapy to start the crawling process
    '''
    def start_requests(self):
        #urls to start the crawling
        urls = ["https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=pcmcat197800050016&st=pcmcat197800050016_categoryid%24cat02001&qp=format_facet%3DFormat~CD%5Egenre_facet%3DGenre~Pop&sp=-bestsellingsort%20skuidsaas",
                "https://www.bestbuy.com/site/searchpage.jsp?cp=1&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=cat02012&st=cat02012_categoryid%24cat02001&qp=genre_facet%3DGenre~New%20Age&sp=-bestsellingsort%20skuidsaas",
                ]
        for url in urls:
            yield  scrapy.Request(url=url, callback=self.parse)
    '''
        parse method to parse the contents of the webpage
    '''
    def parse(self, response):
        #xpath fetching for the list of music
        contents = response.xpath('//*[@id="resultsTabPanel"]/div[3]/div')
        for content in contents:
            #selectors for the needed fields in the page
            title =  content.css('div>h4>a::text').extract_first()
            artist = content.css('.artist>.sku-value::text').extract_first()
            genre = content.css('.genre>.sku-value::text').extract_first()
            rating = content.css('.c-review-average::text').extract_first()
            release = content.css('.release-date>.sku-value::text').extract_first()
            #ordered dict to store in the table
            result = OrderedDict()
            result['Title'] = title
            result['Artist'] = artist
            result['Genre'] = genre
            result['Release'] = release
            result['Rating'] = rating
            yield result
        #links to follow through the next pages
        links = response.css('.pager')
        for l in links:
            if l is not None:
                next_page = l.css('a::attr(href)').extract_first()
                if next_page is not None:
                    yield scrapy.Request(url=next_page, callback=self.parse)
