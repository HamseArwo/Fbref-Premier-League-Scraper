import scrapy
from playerscraper.items import GkItem
# This module is essentially the same as the playerspider. -- planning on using a different website to scrape of players soon so i separated Players and GK --


class GkspiderSpider(scrapy.Spider):
    name = "gkspider"
    allowed_domains = ["fbref.com"]
    start_urls = [
        "https://fbref.com/en/comps/9/2022-2023/2022-2023-Premier-League-Stats"]

    def parse(self, response):
        # Change 2021-2022 to 2022-2023
        table_rows = response.css("#results2022-202391_overall tbody tr")
        for row in table_rows:
            column = row.css("td")
            relative_url = column[0].css("a").attrib["href"]
            team_page = "https://fbref.com/" + relative_url

            current_team = {"team": column[0].css("a::text").get()}

            yield scrapy.Request(team_page, callback=self.parse_team_page, meta={'download_delay': 2.0}, cb_kwargs=current_team)

    def parse_team_page(self, response, **kwargs):
        player_rows = response.css("#stats_standard_9 tbody tr")
        current_team = kwargs["team"]
        for player_row in player_rows:

            # player_column = player_row.css("th")
            player_columns = player_row.css("td")

            position = player_columns[1].css("::text").get()

            apperance = player_columns[3].css("::text").get()

            player_relative_url = player_row.css("th a").attrib["href"]
            player_url = "https://fbref.com" + player_relative_url

            if apperance != "0" and position == "GK":
                gkitem = GkItem()
                gkitem["name"] = player_row.css("th a::text").get()
                gkitem["club"] = current_team

                data = ["position", "age", "apperances"]
                for x in range(3):
                    gkitem[data[x]] = player_columns[x +
                                                     1].css("::text").get()

                yield scrapy.Request(player_url, callback=self.parse_player_page, meta={'download_delay': 2.0}, cb_kwargs={"position": position, "gkitem": gkitem})

    def parse_player_page(self, response, **kwargs):

        gkitem = kwargs["gkitem"]
        # Getting the image of the player
        if response.css(".media-item img::attr(src)").get() is not None:
            player_image = response.css("#meta div")[0]
            gkitem["image"] = player_image.css(
                "img::attr(src)").get()

        else:
            gkitem["image"] = "https://static.wikia.nocookie.net/bts-imagine-fanfic/images/a/ac/Generic-profile-picture.jpg.jpg/revision/latest?cb=20200928042941"
        # Getting the actual stastics of the player

        player_stat_rows = response.css("#stats_keeper_dom_lg  tbody tr")
        index = len(player_stat_rows) - 1

        player_stat_coloumn = player_stat_rows[index].css("td")

        stats = ["mins_played", "ga", "ga_per_90",
                 "SoTA", "saves", "saves_percent", "clean_sheets"]
        columns = [7, 9, 10, 11, 12, 13, 17]

        for stat, column in zip(stats, columns):
            gkitem[stat] = player_stat_coloumn[column].css("::text").get()
        yield gkitem
