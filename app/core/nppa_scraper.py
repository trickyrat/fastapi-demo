import datetime

from bs4 import BeautifulSoup
import requests
import re

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.nertwork_game_audit import NetworkGameAudit
from app.models.nppa_table import NPPATable
from app import crud


class NPPAScraper:
    def __init__(self):
        self.base_url = "https://www.nppa.gov.cn"
        self.data_url = "/nppa/channels/317"  # 第一页 /nppa/channels/317.shtml 后续页面/nppa/channels/317_2.shtml
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44"
        }
        self.suffix = '.shtml'

    def convert_to_soup(self, url: str):
        response = requests.get(url, headers=self.headers)
        response.encoding = 'u8'
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def parse_table(self, url: str) -> list[NPPATable]:
        """ 获取当前页所有审批信息列表

        :return: 审批信息路由列表
        """
        print(f"Start to parse {url}.")
        soup = self.convert_to_soup(url)
        ul = soup.find("ul", "m2nrul")
        links = []
        li_list = ul.find_all("li")
        for li in li_list:
            a = li.find("a")
            title = a.text
            url = f"{self.base_url}{a['href']}"
            publish_date = re.sub(r"[\[\]]", "", li.find("span").text)
            links.append(NPPATable(title=title,
                                   url=url,
                                   publish_date=datetime.datetime.strptime(publish_date, '%Y-%m-%d')))
        print("Parse completed.")
        return links

    def parse_network_game_table(self, url: str, game_type: str) -> list[NetworkGameAudit]:
        """ 处理进口/国产网络游戏审批信息

        :param url: 表格请求路由
        :param game_type: 320 国产 318 进口
        :return: 审批信息列表
        """
        network_games = []
        soup = self.convert_to_soup(url)
        table_rows = soup.find_all('tr', class_='item')
        for row in table_rows:
            tds = row.find_all('td')
            network_games.append(NetworkGameAudit(name=tds[1].text
                                                  , audit_category=tds[2].text
                                                  , publisher=tds[3].text
                                                  , operator=tds[4].text
                                                  , audit_no=tds[5].text
                                                  , isbn=tds[6].text
                                                  , category=1 if game_type == "320" else 2
                                                  ,
                                                  publish_date=datetime.datetime.strptime(tds[7].text, "%Y年%m月%d日")))
        return network_games

    # TODO: 进口电子游戏审批信息

    # TODO: 游戏审批撤销信息

    # TODO: 游戏审批变更信息

    def get_latest(self, url: str, db: Session = Depends(deps.get_db)):
        links = self.parse_table(url)
        crud.nppa_table.multiple_create(db, objs_in=links)
        # 查询数据库判断日期
        # latest_date = crud.nppa_table.get_latest_date(db)
        # filter(lambda x: x['publish_date'] <= latest_date, links)
        # print(links)

    def run(self):
        soup = self.convert_to_soup(self.base_url + self.data_url + self.suffix)
        total_page = re.sub(r"\D", '', soup.find('a', class_='sPage_a sPage_prev').text)
        links_list = []
        for i in range(1, int(total_page) + 1):
            current_page = '' if i == 1 else f'_{i}'
            url = f"{self.base_url}{self.data_url}{current_page}{self.suffix}"
            links_list.append(self.parse_table(url))


if __name__ == '__main__':
    scraper = NPPAScraper()
    # scraper.parse_network_game_table("https://www.nppa.gov.cn/nppa/contents/320/106173.shtml", "320")
    # match = re.search(r"/(\d{3})/", "https://www.nppa.gov.cn/nppa/contents/320/106173.shtml").group(1)
    # scraper.run()
    scraper.get_latest('https://www.nppa.gov.cn/nppa/channels/317.shtml')
