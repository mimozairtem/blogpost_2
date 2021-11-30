import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0108778/'
    ]

    def parse(self, response):
        cast_page = response.css("div.ipc-title__wrapper a").attrib["href"]

        if cast_page:
            cast_page = response.urljoin(cast_page) 
            yield scrapy.Request(cast_page, callback = self.parse_full_credits)
    
    def parse_full_credits(self,response):
        cast_photo_page = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        
        if cast_photo_page:
            for url in cast_photo_page:
                cast_photo = response.urljoin(url)
                yield scrapy.Request(cast_photo, callback= self.parse_actor_page)

    def parse_actor_page(self, response):

        actor_name = response.css("span.itemprop::text").get()
        
        for film in response.css("div.filmo-category-section"):
            movie_or_TV_name = film.css("div.filmo-row a::text").get()

            yield {
            "actor_name" : actor_name,
            "movie_or_TV_name" : movie_or_TV_name
            }

