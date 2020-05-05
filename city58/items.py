# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class City58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Community(scrapy.Item):
    table = 'community'
    id = scrapy.Field()  # 唯一标识
    url = scrapy.Field()
    name = scrapy.Field()  # 小区名
    location = scrapy.Field()  # 粗略所在地
    price = scrapy.Field()  # 每平米均价
    business_area = scrapy.Field()  # 商圈区域
    address = scrapy.Field()  # 详细地址
    households = scrapy.Field()  # 总住户数
    building_age = scrapy.Field()  # 建筑年代
    property_type = scrapy.Field()  # 产权类型
    property = scrapy.Field()  # 产权
    property_fee = scrapy.Field()  # 物业费
    greening_rate = scrapy.Field()  # 绿化率
    parking_nums = scrapy.Field()  # 停车位
    present_sale_rooms = scrapy.Field()  # 目前在售
    present_rent_rooms = scrapy.Field()  # 目前在租


class NewHouse(scrapy.Item):
    table = 'new house'
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()  # 标题
    community = scrapy.Field()  # 所在小区
    total_price = scrapy.Field()  # 总价
    price_per_square_meter = scrapy.Field()  # 单价
    floor = scrapy.Field()  # 所在楼层
    room_type = scrapy.Field()  # 房屋户型
    decoration_type = scrapy.Field()  # 装修情况
    room_area = scrapy.Field()  # 房本面积
    property = scrapy.Field()  # 产权年限
    front_of_house = scrapy.Field()  # 房屋朝向
    building_age = scrapy.Field()  # 建筑年代
    house_type = scrapy.Field()  # 一手房源


class SecondHandHouse(scrapy.Item):
    table = 'second-hand house'
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()  # 标题
    community = scrapy.Field()  # 所在小区
    total_price = scrapy.Field()  # 总价
    price_per_square_meter = scrapy.Field()  # 单价
    floor = scrapy.Field()  # 所在楼层
    room_type = scrapy.Field()  # 房屋户型
    decoration_type = scrapy.Field()  # 装修情况
    room_area = scrapy.Field()  # 房本面积
    property = scrapy.Field()  # 产权年限
    front_of_house = scrapy.Field()  # 房屋朝向
    building_age = scrapy.Field()  # 建筑年代
    house_type = scrapy.Field()  # 一手房源


class Rental(scrapy.Item):
    table = 'rental'
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()  # 标题
    monthly_price = scrapy.Field()  # 月租金
    how_to_pay = scrapy.Field()  # 押一付三
    how_to_rent = scrapy.Field()  # 租赁方式
    community = scrapy.Field()  # 所在小区
    room_type = scrapy.Field()  # 户型
    room_area = scrapy.Field()  # 房本面积
    decoration_type = scrapy.Field()  # 装修情况
    front_of_house = scrapy.Field()  # 房屋朝向
    floor = scrapy.Field()  # 楼层
    location = scrapy.Field()  # 位置
