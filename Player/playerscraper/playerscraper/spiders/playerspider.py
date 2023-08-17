import scrapy
from playerscraper.items import PlayerItem


class PlayerspiderSpider(scrapy.Spider):
    name = "playerspider"

    allowed_domains = ["fbref.com"]
    start_urls = [
        "https://fbref.com/en/comps/9/history/Premier-League-Seasons"]
    position = ""

    def parse(self, response):
        rows = response.css("#seasons tbody tr")
        for row in range(1, 11):
            year = rows[row].css("th a::text").get()
            relative_table_url = rows[row].css("th a").attrib["href"]

            table_page = "https://fbref.com/" + relative_table_url

            yield scrapy.Request(table_page, callback=self.parse_table_page, meta={'download_delay': 2.0}, cb_kwargs={"year": year})

    def parse_table_page(self, response, **kwargs):
        # Change 2021-2022 to 2022-2023
        year = kwargs["year"]

        table_rows = response.css(f"#results{year}91_overall tbody tr")
        for row in table_rows:
            column = row.css("td")
            relative_url = column[0].css("a").attrib["href"]
            team_page = "https://fbref.com/" + relative_url

            current_team = {"team": column[0].css("a::text").get()}

            yield scrapy.Request(team_page, callback=self.parse_team_page, meta={'download_delay': 2.0}, cb_kwargs={"team": column[0].css("a::text").get(), "year": year})

    def parse_team_page(self, response, **kwargs):
        player_rows = response.css("#stats_standard_9 tbody tr")
        current_team = kwargs["team"]
        current_year = kwargs["year"]
        for player_row in player_rows:

            # player_column = player_row.css("th")
            player_columns = player_row.css("td")

            position = player_columns[1].css("::text").get()

            apperance = player_columns[3].css("::text").get()

            player_relative_url = player_row.css("th a").attrib["href"]
            player_url = "https://fbref.com" + player_relative_url

            if apperance != "0" and position != "GK":
                playeritem = PlayerItem()
                playeritem["name"] = player_row.css("th a::text").get()
                playeritem["club"] = current_team
                playeritem["year"] = current_year

                data = ["position", "age", "apperances", "mins_played", "goals", "assist",
                        "ga", "npg", "pkg", "xg", "xast"]
                columns = [1, 2, 3, 5, 7, 8, 9, 10, 11, 15, 17]
                for stat, column in zip(data, columns):
                    playeritem[stat] = player_columns[column].css(
                        "::text").get()
                yield playeritem
                # yield scrapy.Request(player_url, callback=self.parse_player_page, meta={'download_delay': 2.0}, cb_kwargs={"position": position, "playeritem": playeritem})

    def parse_player_page(self, response, **kwargs):

        pass
