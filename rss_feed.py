from dataclasses import dataclass
import json
import requests
import xml.etree.ElementTree as ET

@dataclass
class RSSArticle:
    title: str
    description: str | None
    content: str | None
    link: str
    pub_date: str

    def __post_init__(self):
        self.title = self.title.strip()
        self.description = self.description.strip() if self.description else None
        self.content = self.content.strip() if self.content else None
        self.link = self.link.strip()
        self.pub_date = self.pub_date.strip()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "link": self.link,
            "pub_date": self.pub_date,
        }



class RSSFeedProvider:
    url: str
    id: str

    class FetchFailedError(Exception):
        pass

    @classmethod
    def get_feed(cls) -> list[RSSArticle]:
        r = requests.get(cls.url)
        if r.status_code != 200:
            raise cls.FetchFailedError(f"Failed to fetch {cls.url}")

        root = ET.fromstring(r.text)
        for item in root.findall("./channel/item"):
            content = item.find("content:encoded").text if item.find("content:encoded") is not None else None
            description = item.find("description").text if item.find("description") is not None else None
            yield RSSArticle(
                title=item.find("title").text,
                description=description,
                link=item.find("link").text,
                pub_date=item.find("pubDate").text,
                content=content,
            )

    @classmethod
    def dump(self, filename: str | None = None):
        if not filename:
            filename = f'./{self.id}.json'

        # print(filename)

        feed = [f.to_dict() for f in self.get_feed()]
        with open(filename, 'w') as f:
            json.dump(feed, f)

class TimesOfIndiaProvider(RSSFeedProvider):
    id = "timesofindia"
    url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

class NDTVProvider(RSSFeedProvider):
    id = "ndtv"
    url = "https://feeds.feedburner.com/ndtvnews-top-stories"

class IndiaTodayProvider(RSSFeedProvider):
    id = "indiatoday"
    url = "https://www.indiatoday.in/rss/1206614"

class TheHinduProvider(RSSFeedProvider):
    id = "thehindu"
    url = "https://www.thehindu.com/news/feeder/default.rss"

# class BusinessStandardProvider(RSSFeedProvider):
#     id = "businessstandard"
#     url = "https://www.business-standard.com/rss/india-news-216.rss"