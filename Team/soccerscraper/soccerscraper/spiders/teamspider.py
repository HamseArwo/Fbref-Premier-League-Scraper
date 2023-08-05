import scrapy
from soccerscraper.items import ClubItems


class TeamspiderSpider(scrapy.Spider):
    name = "teamspider"
    allowed_domains = ["fbref.com"]
    start_urls = [
        "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats"]

    def parse(self, response):
        table_rows = response.css("#results2022-202391_overall tbody tr")
        for row in table_rows:
            column = row.css("td")
            clubitem = ClubItems()
            clubitem["rank"] = row.css("th::text").get()

            items = ["match_played", "wins", "draws",
                     "losses", "points", "goal_differences"]
            indexs = [1, 2, 3, 4, 8, 7,]
            for item, index in zip(items, indexs):

                clubitem[item] = column[index].css("::text").get()

                pass

            clubitem["team"] = column[0].css("a::text").get()
            # clubitem["match_played"] = column[1].css("::text").get()
            # clubitem["wins"] = column[2].css("::text").get()
            # clubitem["draws"] = column[3].css("::text").get()
            # clubitem["losses"] = column[4].css("::text").get()
            # clubitem["points"] = column[8].css("::text").get()
            # clubitem["goal_differences"] = column[7].css("::text").get()
            clubitem["top_scorer"] = column[15].css("a::text").get()
            # yield clubitem

            relative_url = column[0].css("a").attrib["href"]
            team_page = "https://fbref.com/" + relative_url
            yield scrapy.Request(team_page, callback=self.parse_teamimage_page, meta={'download_delay': 2.0}, cb_kwargs={"clubitem": clubitem})

    def parse_teamimage_page(self, response, **kwargs):
        clubitem = kwargs["clubitem"]
        clubitem["image"] = response.css(
            "#meta div.logo img::attr(src)").get()
        yield clubitem
