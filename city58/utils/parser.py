import io
import re
import logging
import base64
import hashlib
import requests
from fontTools.ttLib import TTFont
from scrapy.http import Request


def _gen_md5(url):
    """
    将url转换成md5
    :param url:
    :return:
    """
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def _handle_font(base64_str, string):
    """
    处理58同城的字体加密
    :param base64_str:
    :param string:
    :return:
    """
    font = TTFont(io.BytesIO(base64.decodebytes(base64_str.encode())))
    cmap = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    result = []
    try:
        for c in string:
            if ord(c) in cmap:
                text = str(int(cmap[ord(c)][-2:]) - 1)
            else:
                text = c
            result.append(text)
    except Exception as e:
        logging.error(e)
    return ''.join(result)


class Parser(object):

    @classmethod
    def parse_community_detail(cls, response):
        """
        解析小区详情
        :param response:
        :return:
        """
        result = dict()
        try:
            result['id'] = _gen_md5(response.url)
            result['url'] = response.url
            # 小区名
            result['name'] = response.css('.title-bar > span.title::text').extract_first()
            result['location'] = response.css('.title-bar > span.addr::text').extract_first()
            # 房价（元/m2）
            result['price'] = response.css('.price-container > span.price::text').extract_first('-1')
            # 商圈
            result['business_area'] = response.xpath('//table[@class="info-tb"]/tr[1]/td[2]/@title').extract_first()
            # 详细地址
            result['address'] = response.xpath(
                'normalize-space(//table[@class="info-tb"]/tr[1]/td[4]/text())').extract_first()
            # 总住户数
            result['households'] = response.xpath(
                'normalize-space(//table[@class="info-tb"]/tr[2]/td[4]/text())').extract_first()
            # 产权类别
            result['property_type'] = response.xpath('//table[@class="info-tb"]/tr[3]/td[2]/@title').extract_first()
            # 建筑年代
            result['building_age'] = response.xpath('//table[@class="info-tb"]/tr[5]/td[2]/@title').re_first(r'\d+')
            # 产权
            result['property'] = response.xpath('//table[@class="info-tb"]/tr[4]/td[2]/@title').extract_first()
            # 停车位
            result['parking_nums'] = response.xpath('//table[@class="info-tb"]/tr[6]/td[4]/@title').extract_first()
            # 目前在售
            result['present_sale_rooms'] = response.css('tr[class="tb-btm"]').css(
                'td:nth-child(2) > a > span::text').re_first(r'\d+')
            # 目前在租
            result['present_rent_rooms'] = response.css('tr[class="tb-btm"]').css(
                'td:nth-child(4) > a > span::text').re_first(r'\d+')
        except Exception as e:
            logging.error(e)
        return result

    @classmethod
    def parse_second_hand_house_detail(cls, response):
        """
        解析二手房信息
        :param response:
        :return: 二手房信息
        """
        result = dict()
        try:
            base64_str = re.findall(r"charset=utf-8;base64,(.*?)'\)", response.text)[0]

            result['id'] = _gen_md5(response.url)
            result['url'] = response.url
            # 标题
            title_str = response.css('body > div.main-wrap > div.house-title > h1::text').extract_first()
            result['title'] = _handle_font(base64_str, title_str)
            # 小区
            result['community'] = response.css(
                '.house-basic-right.fr > ul > li:nth-child(1) > span.c_000.mr_10 > a::text').extract_first().strip()
            # 细节
            shh_detail = response.css('#generalSituation > div')
            # 总价和每平米单价
            price_str = response.css(
                'ul.general-item-left > li:nth-child(1) > span.c_000.strongbox::text').extract_first().strip()
            price_str = _handle_font(base64_str, price_str)
            result['total_price'] = price_str[:price_str.find('(')]
            result['price_per_square_meter'] = price_str[price_str.find('(') + 1:price_str.find(')')]
            # 所在楼层
            result['floor'] = shh_detail.css(
                'ul.general-item-right > li:nth-child(1) > span.c_000::text').extract_first()
            # 房屋户型
            result['room_type'] = shh_detail.css(
                'ul.general-item-left > li:nth-child(2) > span.c_000::text').extract_first()
            # 装修情况
            result['decoration_type'] = shh_detail.css(
                'ul.general-item-right > li:nth-child(2) > span.c_000::text').extract_first()
            # 房本面积
            result['room_area'] = shh_detail.css(
                'ul.general-item-left > li:nth-child(3) > span.c_000::text').extract_first()
            # 产权年限
            result['property'] = shh_detail.css(
                'ul.general-item-right > li:nth-child(3) > span.c_000::text').extract_first()
            # 房屋朝向
            result['front_of_house'] = shh_detail.css(
                'ul.general-item-left > li:nth-child(4) > span.c_000::text').extract_first()
            # 建筑年代
            result['building_age'] = shh_detail.css(
                'ul.general-item-right > li:nth-child(4) > span.c_000::text').extract_first()
            # 一手房源
            result['house_type'] = shh_detail.css(
                'ul.general-item-left > li:nth-child(5) > span.c_000::text').extract_first()
        except Exception as e:
            logging.error(e)
        return result

    @classmethod
    def parse_rental_detail(cls, response):
        """
        解析租房信息
        :param response:
        :return:
        """
        result = dict()
        try:
            base64_str = re.findall(r"charset=utf-8;base64,(.*?)'\)", response.text)[0]
            result['id'] = _gen_md5(response.url)
            result['url'] = response.url
            # 标题
            title_str = response.css('body > div.main-wrap > div.house-title > h1::text').extract_first()
            result['title'] = _handle_font(base64_str, title_str)
            # 月租
            price_str = response.css(
                '.house-desc-item.fl.c_333 > div > span.c_ff552e > b::text').extract_first()
            result['monthly_price'] = _handle_font(base64_str, price_str)
            # 付款方式
            result['how_to_pay'] = response.css(
                '.house-desc-item.fl.c_333 > div > span.instructions::text').extract_first()
            # 租赁方式
            result['how_to_rent'] = response.css(
                '.house-desc-item.fl.c_333 > ul > li:nth-child(1) > span:nth-child(2)::text').extract_first()
            # 小区
            result['community'] = response.css(
                '.house-desc-item.fl.c_333 > ul > li:nth-child(4) > span:nth-child(2) > a::text').extract_first().strip()
            # 房屋户型、房本面积、装修情况
            house_str = response.css(
                '.house-desc-item.fl.c_333 > ul > li:nth-child(2) > span.strongbox::text').extract_first()
            house_str = _handle_font(base64_str, house_str).replace('\xa0\xa0', '/').replace(' ', '').split('/')
            result['room_type'] = house_str[0]
            result['room_area'] = house_str[1]
            result['decoration_type'] = house_str[2]
            # 房屋朝向、所在楼层
            floor_str = response.css(
                '.house-desc-item.fl.c_333 > ul > li:nth-child(3) > span.strongbox::text').extract_first().strip()
            floor_str = _handle_font(base64_str, floor_str).replace('\xa0\xa0', '/').replace(' ', '').split('/', 1)
            result['front_of_house'] = floor_str[0]
            result['floor'] = floor_str[1]
            # 位置
            result['location'] = response.css(
                '.house-desc-item.fl.c_333 > ul > li:nth-child(6) > span.dz::text').extract_first().strip()
        except Exception as e:
            logging.error(e)
        return result


if __name__ == '__main__':
    def test_parse_community_detail():
        """
        测试小区信息是否返回正确
        :return:
        """
        url = 'https://hz.58.com/xiaoqu/lvchenglanting/'
        Request(url=url,
                callback=Parser.parse_community_detail)


    def test_parse_second_hand_house_detail():
        """
        测试二手房信息是否返回正确
        :return:
        """
        url = 'https://hz.58.com/ershoufang/42055990636693x.shtml'
        Request(url=url,
                callback=Parser.parse_second_hand_house_detail)


    def test_parse_rental_detail():
        """
        测试租房信息是否返回正确
        :return:
        """
        url = 'https://hz.58.com/zufang/41827113289999x.shtml'
        Request(url=url,
                callback=Parser.parse_rental_detail)


    # 测试
    # test_parse_community_detail
    # test_parse_second_hand_house_detail()
    test_parse_rental_detail()
