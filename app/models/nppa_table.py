from typing import TYPE_CHECKING
import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.db.base_class import Base


class NPPATable(Base):
    # def __init__(self, title: str, url: str, publish_date: str):
    #     self.title = title
    #     self.url = url
    #     self.publish_date = datetime.datetime.strptime(publish_date, "%Y-%m-%d")

    def __gt__(self, other):
        return self.publish_date > other.publish_date

    def __lt__(self, other):
        return self.publish_date < other.publish_date

    def __str__(self):
        return f"title: {self.title}, url: {self.url}, publish_date: {self.publish_date}"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), unique=True, index=True)
    url = Column(String(512), unique=True, index=True)
    publish_date = Column(DateTime)
