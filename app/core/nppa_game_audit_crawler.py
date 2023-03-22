import datetime
import logging

from bs4 import BeautifulSoup
import requests
import re

from sqlalchemy.orm import Session

from app.api import deps
from app.models import EGameAudit, GameAuditCancel, GameAuditChange
from app.models.network_game_audit import NetworkGameAudit
from app.models.game_audit import GameAudit
from app import crud


class NPPAGameAuditCrawler:
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

    def parse_table(self, url: str) -> list[GameAudit]:
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
            links.append(GameAudit(title=title,
                                   url=url,
                                   publish_date=datetime.datetime.strptime(publish_date, '%Y-%m-%d')))
        logging.info("Parse completed.")
        return links

    def parse_network_game_audits(self, url: str, game_type: str) -> list[NetworkGameAudit]:
        """ 解析进口/国产网络游戏审批信息

        :param url: 表格请求路由
        :param game_type: 320 国产 318 进口
        :return: 审批信息列表
        """
        logging.info(f"Start to parse network game audit, url: {url}.")
        network_games = []
        soup = self.convert_to_soup(url)
        table_rows = soup.select('tr:not([style*=color])')
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
        logging.info(f"Parsed total {len(network_games)} network game audits from url: {url}.")
        return network_games

    def parse_egame_audits(self, url: str) -> list[EGameAudit]:
        """
        解析进口电子游戏审批信息

        :param url: 表格请求路由 319
        :return: 进口电子游戏审批信息列表
        """
        logging.info(f"Start to parse e-game audit, url: {url}.")
        egames = []
        soup = self.convert_to_soup(url)
        table_rows = soup.select('tr:not([style*=color])')
        for row in table_rows:
            tds = row.find_all('td')
            egames.append(EGameAudit(name=tds[1].text,
                                     publisher=tds[2].text,
                                     audit_no=tds[3].text,
                                     publish_date=datetime.datetime.strptime(tds[4].text, "%Y年%m月%d日")))

        logging.info(f"Parsed total {len(egames)} e-game audits from url: {url}.")
        return egames

    def parse_game_audit_cancels(self, url: str) -> list[GameAuditCancel]:
        """
        解析游戏审批撤销信息

        :param url: 表格请求路由 747
        :return: 游戏审批撤销信息列表
        """
        logging.info(f"Start to parse game cancel audit, url: {url}.")
        cancellations = []
        soup = self.convert_to_soup(url)
        table_rows = soup.select('tr:not([style*=color])')
        for row in table_rows:
            tds = row.find_all('td')
            td_count = len(tds)
            isbn = '' if td_count == 8 else tds[7].text
            approve_date = tds[7].text if td_count == 8 else tds[8].text
            cancellations.append(GameAuditCancel(name=tds[1].text,
                                                 audit_category=tds[2].text,
                                                 publisher=tds[3].text,
                                                 operator=tds[4].text,
                                                 cancel_msg=tds[5].text,
                                                 audit_no=tds[6].text,
                                                 isbn=isbn,
                                                 approve_date=datetime.datetime.strptime(approve_date, "%Y年%m月%d日")))
        logging.info(f"Parsed total {len(cancellations)} game cancel audits from url: {url}.")
        return cancellations

    def parse_game_audit_changes(self, url: str) -> list[GameAuditChange]:
        """
        解析游戏审批变更信息

        :param url: 表格请求路由 321
        :return: 游戏审批变更信息列表
        """
        logging.info(f"Start to parse game change audit, url: {url}.")
        changes = []
        soup = self.convert_to_soup(url)
        table_rows = soup.select('tr:not([style*=color])')
        for row in table_rows:
            tds = row.find_all('td')
            td_count = len(tds)
            isbn = '' if td_count == 8 else tds[7].text
            publish_date = tds[7].text if td_count == 8 else tds[8].text
            changes.append(GameAuditChange(name=tds[1].text,
                                           audit_category=tds[2].text,
                                           publisher=tds[3].text,
                                           operator=tds[4].text,
                                           change_msg=tds[5].text,
                                           audit_no=tds[6].text,
                                           isbn=isbn,
                                           change_date=datetime.datetime.strptime(publish_date, "%Y年%m月%d日")))

        logging.info(f"Parsed total {len(changes)} game change audits from url: {url}.")
        return changes

    def get_latest_game_audits(self, db: Session):

        links = self.parse_table(self.base_url + self.data_url + self.suffix)
        latest_date = crud.game_audit.get_latest_date(db)
        links = list(filter(lambda x: x.publish_date > latest_date, links))
        # save links
        if links:
            crud.game_audit.multiple_create(db, objs_in=links)
            logging.info(f"Saved total {len(links)} game audits")
            self.parse_game_audits(links)
        else:
            logging.info("No NPPA game audit to save.")

    def get_all_game_audits(self, db: Session):
        is_empty = crud.game_audit.is_empty(db)
        if not is_empty:
            crud.game_audit.delete_all(db)  # clear database table

        soup = self.convert_to_soup(self.base_url + self.data_url + self.suffix)
        total_page = re.sub(r"\D", '', soup.find('a', class_='sPage_a sPage_prev').text)
        game_audit_list = []
        for i in range(1, int(total_page) + 1):
            current_page = '' if i == 1 else f'_{i}'
            url = f"{self.base_url}{self.data_url}{current_page}{self.suffix}"
            game_audit_list.extend(self.parse_table(url))
        if game_audit_list:
            crud.game_audit.multiple_create(db, objs_in=game_audit_list)
            logging.info(f"Saved total {len(game_audit_list)} game audits")
            self.parse_game_audits(db, game_audit_list)
        else:
            logging.info("No NPPA game audit to save.")

    def parse_game_audits(self, db: Session, game_audits: list[GameAudit]) -> None:
        domestic_network_game_cnt = foreign_network_game_cnt = audit_changes_cnt = audit_cancel_cnt = egame_audit_cnt = 0
        for audits in game_audits:
            data_type = re.search(r"/(\d{3})/", audits.url).group(1)
            if data_type == '318':
                domestic_network_games = self.parse_network_game_audits(audits.url, data_type)
                domestic_network_game_cnt += len(domestic_network_games)
                crud.network_game_audit.multiple_create(db, objs_in=domestic_network_games)
            elif data_type == '320':
                foreign_network_games = self.parse_network_game_audits(audits.url, data_type)
                foreign_network_game_cnt += len(foreign_network_games)
                crud.network_game_audit.multiple_create(db, objs_in=foreign_network_games)
            elif data_type == '321':
                audit_changes = self.parse_game_audit_changes(audits.url)
                audit_changes_cnt += len(audit_changes)
                crud.game_audit_change.multiple_create(db, objs_in=audit_changes)
            elif data_type == '747':
                audit_cancels = self.parse_game_audit_cancels(audits.url)
                audit_cancel_cnt += len(audit_cancels)
                crud.game_audit_cancel.multiple_create(db, objs_in=audit_cancels)
            elif data_type == '319':
                egames = self.parse_egame_audits(audits.url)
                egame_audit_cnt += len(egames)
                crud.egame_audit.multiple_create(db, objs_in=egames)

        logging.info(f"Saved total {domestic_network_game_cnt} domestic network games.")
        logging.info(f"Saved total {foreign_network_game_cnt} foreign network games.")
        logging.info(f"Saved total {audit_changes_cnt} game audit changes.")
        logging.info(f"Saved total {audit_cancel_cnt} game audit cancels.")
        logging.info(f"Saved total {egame_audit_cnt} foreign e-games.")

    def run(self, mode=1):
        """
        :param mode 1 获取最新数据 2 获取全量数据
        """
        db: Session = next(deps.get_db())
        if mode == 1:
            self.get_latest_game_audits(db)
        else:
            self.get_all_game_audits(db)


def init_log():
    logging.basicConfig(level='INFO')
    logger = logging.getLogger('nppa_game_audit_scraper_logger')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level="DEBUG")
    console_log_format = "%(name)s--->%(asctime)--->%(message)--->%(lineno)d"
    formatter = logging.Formatter(fmt=console_log_format)
    console_handler.setFormatter(fmt=formatter)
    logger.addHandler(console_handler)


if __name__ == '__main__':
    init_log()
    scraper = NPPAGameAuditCrawler()
    scraper.run(2)
