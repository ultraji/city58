import requests
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.cmdline import execute
from city58.utils.parser import Parser
from city58.items import Community, SecondHandHouse, NewHouse, Rental


class City58Spider(scrapy.Spider):
    name = 'city58'
    allowed_domains = ['58.com']
    debug_flag = False

    def start_requests(self):
        city_url = 'https://{}.58.com/xiaoqu/'.format(self.settings.get('CITY'))
        region_url = city_url + '{}/'

        response = Selector(requests.get(city_url))

        region_code_list = response.css('.filter-wrap dl:nth-child(1) dd > a::attr(value)').extract()
        region_url_list = list()  # 行政区URL列表
        if region_code_list:
            for region_code in region_code_list:
                if region_code:
                    region_url_list.append(region_url.format(str(region_code)))

        for region_url in region_url_list:
            if region_url:
                yield Request(url=region_url+'pn_1/',
                              callback=self.parse_region_page,
                              errback=self.error_back,
                              priority=10)
                if self.debug_flag:
                    break

    def parse_region_page(self, response):
        """
        从行政区页面中遍历所有小区列表
        https://hz.58.com/xiaoqu/86/pn_1/
        :param response:
        :return:
        """
        community_url_list = response.css(
            '.content-side-left > ul > li > div.list-info > h2 > a::attr(href)').extract()
        if community_url_list:
            for community_url in community_url_list:
                if community_url:
                    yield Request(url=community_url,
                                  callback=self.parse_community_page_detail,
                                  errback=self.error_back,
                                  priority=3)
                    if self.debug_flag:
                        break

        next_page = response.css('a[class="nextPage"]')
        if False and next_page:
            s = response.url
            s = s[:s.rfind('_')+1] + str(int(s[s.rfind('_')+1:-1]) + 1) + '/'
            next_url = s
            yield Request(url=next_url,
                          callback=self.parse_region_page,
                          errback=self.error_back,
                          priority=9)

    def parse_community_page_detail(self, response):
        """
        :param response:
        :return:
        """
        # 抛出小区详细信息
        community_item = Community()
        community_detail = Parser.parse_community_detail(response)
        community_item.update(community_detail)
        yield community_item

        # 接着遍历二手房信息列表
        second_hand_house_list_url = response.url + 'ershoufang/pn_1/'
        yield Request(url=second_hand_house_list_url,
                      callback=self.parse_community_ssh_page,
                      errback=self.error_back,
                      priority=8)

        # 接着遍历出租房信息列表
        rental_list_url = response.url + 'chuzu/pn_1/'
        yield Request(url=rental_list_url,
                      callback=self.parse_community_rental_page,
                      errback=self.error_back,
                      priority=8)

    def parse_community_ssh_page(self, response):
        """
        获取二手房URL列表
        :param response:
        :return:
        """
        shh_url_list = response.css(
            '.listwrap > table > tr > td.t > a.t::attr(href)').extract()
        if shh_url_list:
            for shh_url in shh_url_list:
                if shh_url:
                    yield Request(url=shh_url,
                                  callback=self.parse_shh_detail,
                                  errback=self.error_back,
                                  priority=6)
                    if self.debug_flag:
                        break

        next_page = response.css('a[class="next"]')
        if next_page:
            s = response.url
            s = s[:s.rfind('_') + 1] + str(int(s[s.rfind('_') + 1:-1]) + 1) + '/'
            next_url = s
            yield Request(url=next_url,
                          callback=self.parse_community_ssh_page,
                          errback=self.error_back,
                          priority=7)

    def parse_community_rental_page(self, response):
        """
        获取出租房URL列表
        :param response:
        :return:
        """
        rental_url_list = response.css(
            '.listwrap > table > tr > td.t > a.t::attr(href)').extract()
        if rental_url_list:
            for rental_url in rental_url_list:
                if rental_url:
                    yield Request(url=rental_url,
                                  callback=self.parse_rental_detail,
                                  errback=self.error_back,
                                  priority=6)
                    if self.debug_flag:
                        break
        next_page = response.css('a[class="next"]')
        if next_page:
            s = response.url
            s = s[:s.rfind('_') + 1] + str(int(s[s.rfind('_') + 1:-1]) + 1) + '/'
            next_url = s
            yield Request(url=next_url,
                          callback=self.parse_community_rental_page,
                          errback=self.error_back,
                          priority=7)

    def parse_shh_detail(self, response):
        """
        :param response:
        :return:
        """
        shh_item = SecondHandHouse()
        shh_detail = Parser.parse_second_hand_house_detail(response)
        shh_item.update(shh_detail)
        yield shh_item

    def parse_rental_detail(self, response):
        """
        :param response:
        :return:
        """
        rental_item = Rental()
        rental_detail = Parser.parse_rental_detail(response)
        rental_item.update(rental_detail)
        yield rental_item

    def error_back(self, e):
        """
        数据收集器记录失败请求
        """
        _ = self
        self.crawler.stats.inc_value("Failed_Request")


if __name__ == '__main__':
    execute("scrapy crawl city58".split())
