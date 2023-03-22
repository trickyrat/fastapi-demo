import datetime
import logging

from bs4 import BeautifulSoup
import requests
import re

from sqlalchemy.orm import Session

from app.api import deps
from app.models import EGameAudit, AuditCancel, AuditChange
from app.models.network_game_audit import NetworkGameAudit
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
        logging.info(f"Start to parse {url}.")
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
        logging.info("Parse completed.")
        return links

    def parse_network_game_table(self, url: str, game_type: str) -> list[NetworkGameAudit]:
        """ 解析进口/国产网络游戏审批信息

        :param url: 表格请求路由
        :param game_type: 320 国产 318 进口
        :return: 审批信息列表
        """
        network_games = []
        soup = self.convert_to_soup(url)
        table_rows = soup.find_all('tr', class_='item')
        for row in table_rows:
            tds = row.find_all('td')
            td_count = len(tds)
            isbn = '' if td_count == 7 else tds[6].text
            category = 1 if game_type == "320" else 2
            publish_date = tds[6].text if td_count == 7 else tds[7].text
            network_games.append(NetworkGameAudit(name=tds[1].text,
                                                  audit_category=tds[2].text,
                                                  publisher=tds[3].text,
                                                  operator=tds[4].text,
                                                  audit_no=tds[5].text,
                                                  isbn=isbn,
                                                  category=category,
                                                  publish_date=datetime.datetime.strptime(publish_date,
                                                                                          "%Y年%m月%d日")))
        return network_games

    def parse_egame_table(self, url: str) -> list[EGameAudit]:
        """
        解析进口电子游戏审批信息

        :param url: 表格请求路由 319
        :return: 进口电子游戏审批信息列表
        """
        games = []
        soup = self.convert_to_soup(url)
        table_rows = soup.find_all('tr:not([style*=color])')
        for row in table_rows:
            tds = row.find_all('td')
            games.append(EGameAudit(name=tds[1].text,
                                    publisher=tds[2].text,
                                    audit_no=tds[3].text,
                                    publish_date=datetime.datetime.strptime(tds[4].text, "%Y年%m月%d日")))
        return games

    def parse_game_audit_cancel_table(self, url: str) -> list[AuditCancel]:
        """
        解析游戏审批撤销信息

        :param url: 表格请求路由 747
        :return: 游戏审批撤销信息列表
        """
        cancellations = []
        soup = self.convert_to_soup(url)
        table_rows = soup.select('tr:not([style*=color])')
        for row in table_rows:
            tds = row.find_all('td')
            cancellations.append(AuditCancel(name=tds[1].text,
                                             audit_category=tds[2].text,
                                             publisher=tds[3].text,
                                             operator=tds[4].text,
                                             cancel_msg=tds[5].text,
                                             audit_no=tds[6].text,
                                             isbn=tds[7].text,
                                             approve_date=datetime.datetime.strptime(tds[8].text, "%Y年%m月%d日")))
        return cancellations

    def parse_game_audit_change_table(self, url: str) -> list[AuditChange]:
        """
        解析游戏审批变更信息

        :param url: 表格请求路由 321
        :return: 游戏审批变更信息列表
        """
        changes = []
        soup = self.convert_to_soup(url)
        table_rows = soup.find_all('tr:not([style*=color])')
        for row in table_rows:
            tds = row.find_all('td')
            changes.append(AuditChange(name=tds[1].text,
                                       audit_category=tds[2].text,
                                       publisher=tds[3].text,
                                       operator=tds[4].text,
                                       change_msg=tds[5].text,
                                       audit_no=tds[6].text,
                                       isbn=tds[7].text,
                                       change_date=datetime.datetime.strptime(tds[8].text, "%Y年%m月%d日")))
        return changes

    def get_latest_nppas(self):
        db: Session = next(deps.get_db())
        links = self.parse_table(self.base_url + self.data_url + self.suffix)
        latest_date = crud.nppa_table.get_latest_date(db)
        links = list(filter(lambda x: x.publish_date > latest_date, links))
        # save links
        if links:
            crud.nppa_table.multiple_create(db, objs_in=links)
            logging.info(f"Saved total {len(links)} links")
            self.parse_nppas(links)
        else:
            logging.info("No NPPA data to save.")

    def get_all_nppas(self):
        db: Session = next(deps.get_db())
        is_empty = crud.nppa_table.is_empty(db)
        if not is_empty:
            crud.nppa_table.delete_all(db)  # clear database table

        soup = self.convert_to_soup(self.base_url + self.data_url + self.suffix)
        total_page = re.sub(r"\D", '', soup.find('a', class_='sPage_a sPage_prev').text)
        links_list = []
        for i in range(1, int(total_page) + 1):
            current_page = '' if i == 1 else f'_{i}'
            url = f"{self.base_url}{self.data_url}{current_page}{self.suffix}"
            links_list.extend(self.parse_table(url))
        if links_list:
            crud.nppa_table.multiple_create(db, objs_in=links_list)
            logging.info(f"Saved total {len(links_list)} links")
            # self.parse_nppas(links_list)
        else:
            logging.info("No NPPA date to save.")

    def parse_nppas(self, nppas: list[NPPATable]) -> None:
        db: Session = next(deps.get_db())
        domestic_network_game_count = foreign_network_game_count = audit_changes_count = audit_cancel_count \
            = egame_audit_count = 0
        for nppa in nppas:
            data_type = re.search(r""
                                  r"", nppa.url).group(1)
            if data_type == '318':
                domestic_network_games = self.parse_network_game_table(nppa.url, data_type)
                domestic_network_game_count += len(domestic_network_games)
                crud.network_game_audit.multiple_create(db, objs_in=domestic_network_games)
            elif data_type == '320':
                foreign_network_games = self.parse_network_game_table(nppa.url, data_type)
                foreign_network_game_count += len(foreign_network_games)
                crud.network_game_audit.multiple_create(db, objs_in=foreign_network_games)
            elif data_type == '321':
                audit_changes = self.parse_game_audit_change_table(nppa.url)
                audit_changes_count += len(audit_changes)
                crud.audit_change.multiple_create(db, objs_in=audit_changes)
            elif data_type == '747':
                audit_cancels = self.parse_game_audit_cancel_table(nppa.url)
                audit_cancel_count += len(audit_cancels)
                crud.audit_change.multiple_create(db, objs_in=audit_cancels)
            elif data_type == '319':
                egames = self.parse_egame_table(nppa.url)
                egame_audit_count += len(egames)
                crud.egame_audit.multiple_create(db, objs_in=egames)

        logging.info(f"Saved total {domestic_network_game_count} domestic network games.")
        logging.info(f"Saved total {foreign_network_game_count} foreign network games.")
        logging.info(f"Saved total {audit_changes_count} audit changes.")
        logging.info(f"Saved total {audit_cancel_count} audit cancels.")
        logging.info(f"Saved total {egame_audit_count} foreign egame.")

    def parse_all_tables(self) -> None:
        """解析所有数据
        """
        db: Session = next(deps.get_db())
        nppas = crud.nppa_table.get_all(db)
        self.parse_nppas(nppas)

    def run(self, mode=1):
        """
        :param mode 1 获取最新数据 2 获取全量数据
        """
        if mode == 1:
            self.get_latest_nppas()
        else:
            self.get_all_nppas()


def init_log():
    logging.basicConfig(level='INFO')
    logger = logging.getLogger('nppa_scraper_logger')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level="DEBUG")
    console_log_format = "%(name)s--->%(asctime)--->%(message)--->%(lineno)d"
    formatter = logging.Formatter(fmt=console_log_format)
    console_handler.setFormatter(fmt=formatter)
    logger.addHandler(console_handler)


if __name__ == '__main__':
    init_log()
    scraper = NPPAScraper()
    scraper.run(2)
