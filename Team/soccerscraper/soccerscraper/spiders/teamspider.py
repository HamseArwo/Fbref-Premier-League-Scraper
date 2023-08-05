import scrapy
from soccerscraper.items import ClubItems


class TeamspiderSpider(scrapy.Spider):
    name = "teamspider"
    allowed_domains = ["fbref.com"]
    start_urls = [
        "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats"]

    def parse(self, response):

        # Getting all the rows from the teams table

        table_rows = response.css("#results2022-202391_overall tbody tr")
# Looping through each row
        for row in table_rows:
            column = row.css("td")
            clubitem = ClubItems()
# Storing the rank data into the scrapy Item
            clubitem["rank"] = row.css("th::text").get()

            items = ["match_played", "wins", "draws",
                     "losses", "points", "goal_differences"]
            indexs = [1, 2, 3, 4, 8, 7,]
        #    Within the row looping through each spefiic columns then storing the data into the scrapy item
        # The columns are specified by the index array
            for item, index in zip(items, indexs):
                clubitem[item] = column[index].css("::text").get()
                pass

            clubitem["team"] = column[0].css("a::text").get()
            clubitem["top_scorer"] = column[15].css("a::text").get()


# Getting the url to go into the Teams page
            relative_url = column[0].css("a").attrib["href"]
            team_page = "https://fbref.com/" + relative_url
# Tell the spider to go into the teams page
# Once it has the data go to the parse_teamimage_page function
# Pass the clubItem object as a kwarg arugement
            yield scrapy.Request(team_page, callback=self.parse_teamimage_page, meta={'download_delay': 2.0}, cb_kwargs={"clubitem": clubitem})

    def parse_teamimage_page(self, response, **kwargs):

        # Unpack the clubitem
        clubitem = kwargs["clubitem"]
        # Get the image
        clubitem["image"] = response.css(
            "#meta div.logo img::attr(src)").get()
        # Yield the clubItem object
        yield clubitem
