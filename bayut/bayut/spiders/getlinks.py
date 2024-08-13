## get all links for each property

import scrapy


class GetlinksSpider(scrapy.Spider):
    name = 'getlinks'

    BASE_URL = "https://www.bayut.eg"
    start_urls = [
        f"https://www.bayut.eg/en/egypt/properties-for-sale/page-{i}/" for i in range(2, 5)
    ]

    def parse(self, response):
        divs = response.css("div._611e70d3 a::attr(href)").getall()  # get the first div
        ## get data from each link
        for url in divs:
            yield scrapy.Request(url=self.BASE_URL+url, callback=self.parsepage)

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