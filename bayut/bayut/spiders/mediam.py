## get all links for each property

import scrapy


class GetlinksSpider(scrapy.Spider):
    name = 'getlinks'


    start_urls = [
       "file:///C:/Users/zeiad/AppData/Local/Temp/MicrosoftEdgeDownloads/7a422e69-8d8e-4722-a9dc-c908625d0414/medium_search_why_we_invested.html"
    ]

    def parse(self, response):
        divs = response.css("div.zq.l div.ab div.l.rv.fk").getall() 

        ##get first a tag in each div
        links=[]
        for div in divs:
            a = div.css("a::attr(href)").get()
            links.append(a)
        print("ziad",len(links))


        
        print("ziad",len(divs))
         # get the first div
        ## get data from each link
        # for url in divs:
        #     yield scrapy.Request(url=self.BASE_URL+url, callback=self.parsepage)

    def parsepage(self, response):


        main_img= response.css(".febd06cb img::attr(src)").get()
        rest_imgs = response.css(".d67fbd0a img::attr(src)").getall()
        price = response.css('._105b8a67::text').get()
        attrs=response.css('._6f6bb3bc ::text').getall()
        print("ziad",attrs,price,main_img,rest_imgs)
        yield {
            "main_img": main_img,

            "price": price,

        

        }