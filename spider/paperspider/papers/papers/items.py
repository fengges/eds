# -*- coding: utf-8 -*-

import scrapy


class PapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JournalItem(scrapy.Item):
    # define the fields for your item here like:
    ISSN = scrapy.Field()
    IF = scrapy.Field()
    ave_if = scrapy.Field()
    cn_name = scrapy.Field()
    en_name = scrapy.Field()
    former_name = scrapy.Field()
    countryOrRegion = scrapy.Field()
    discipline_subject = scrapy.Field()
    self_cited_rate = scrapy.Field()
    url = scrapy.Field()
    cited_num = scrapy.Field()
    pass


class PaperItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    abstract = scrapy.Field()
    org = scrapy.Field()
    year = scrapy.Field()
    cited_num = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field("")
    author = scrapy.Field()
    author_id = scrapy.Field()
    cited_url = scrapy.Field()
    reference_url = scrapy.Field()
    paper_md5 = scrapy.Field()
    pass


class UpdateAbstractItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    abstract = scrapy.Field()
    org = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field("")
    pass


class UpdateInstitutionItem(scrapy.Item):
    _id = scrapy.Field()
    author = scrapy.Field()
    pass


class CNKIZhuanliItem(scrapy.Item):
    title = scrapy.Field()
    abstract = scrapy.Field()
    author_list = scrapy.Field()
    url = scrapy.Field()
    proposer = scrapy.Field()
    date1 = scrapy.Field()
    date2 = scrapy.Field()
    search_id = scrapy.Field()
    pass


class CNKIABSTRACTItem(scrapy.Item):
    id = scrapy.Field()
    abstract = scrapy.Field()
    ip_content = scrapy.Field()
    pass


class PSSZhuanliItem(scrapy.Item):
    INVIEW = scrapy.Field()
    PAVIEW = scrapy.Field()
    TIVIEW = scrapy.Field()
    ABSTRACT = scrapy.Field()
    APD = scrapy.Field()
    AP = scrapy.Field()
    PD = scrapy.Field()
    PN = scrapy.Field()
    _ID = scrapy.Field()
    search_id = scrapy.Field()
    pass


class TermItem(scrapy.Item):
    id = scrapy.Field()
    term = scrapy.Field()
    pass


class JiechuItem(scrapy.Item):
    name = scrapy.Field()
    year = scrapy.Field()
    detail = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    pass
