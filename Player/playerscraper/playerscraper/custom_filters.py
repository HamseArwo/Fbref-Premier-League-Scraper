# custom_filters.py

from scrapy.dupefilters import RFPDupeFilter


class AlwaysUniqueDupeFilter(RFPDupeFilter):
    def request_seen(self, request):
        return False
