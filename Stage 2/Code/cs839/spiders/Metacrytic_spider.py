import scrapy
from collections import OrderedDict
class MetacryticSpider(scrapy.Spider):
    name ="metacrytic"
    '''
        initial method called by the scrapy to set the crawling process
    '''
    def start_requests(self):
        #base url's to start the spider
        urls = ["http://www.metacritic.com/browse/albums/genre/date/pop",
                "http://www.metacritic.com/browse/albums/genre/date/rock?view=condensed",
                ]
        for url in urls:
            yield  scrapy.Request(url=url, callback=self.parse)
    '''
       Parse method specific to parse the contents of a particular music from a page 
    '''
    def parse_music(self,response):
        #title xpath from the page
        title = response.xpath('//*[@id="main"]/div/div[1]/div[2]/a/span/h1/text()').extract_first()
        #artist xpath from the page
        artist = response.xpath('//*[@id="main"]/div/div[1]/div[3]/a/span/text()').extract_first()
        #genres list xpath from the page
        genres = response.xpath('//*[@id="main"]/div/div[3]/div/div[2]/div[2]/div[2]/ul/li[2]/span')
        genre = ''
        for ind,g in enumerate(genres):
            if ind>1:
                genre= genre+','
            if ind>0:
                genre = genre + g.xpath('text()').extract_first()
        #ratings xpath from the page
        rating = response.xpath('//*[@id="main"]/div/div[3]/div/div[2]/div[1]/div[2]/div[1]/div/a/div/text()').extract_first()
        #release xpath from the page
        release = response.xpath('//*[@id="main"]/div/div[1]/div[4]/ul/li[2]/span[2]/text()').extract_first()
       
        #ordered dict to put the results in the dict
        result = OrderedDict()
        result['Title'] = title
        result['Artist']= artist
        result['Genre']= genre
        result['Release']= release
        result['Rating']= rating
        yield result
    '''
        parse method to parse the music listing page
    '''
    def parse(self, response):
        contents = response.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/div[3]/div[2]/ol/li')
        for content in contents:#iterate through the list of music
            content_page = content.css('a::attr(href)').extract_first()
            if content_page is not None:
                content_page = response.urljoin(content_page)  # to handle relative paths
                yield scrapy.Request(url=content_page, callback=self.parse_music)#crawl the specific music page
        #spider link for the next page
        next_page = response.xpath('//*[@id="main"]/div[1]/div[2]/div/div[1]/span[2]')
        next_page_link = next_page.css('a::attr(href)').extract_first()
        if next_page_link is not None:
            next_page_link = response.urljoin(next_page_link)  # to handle relative paths
            yield scrapy.Request(url=next_page_link, callback=self.parse)#set the follow pages
