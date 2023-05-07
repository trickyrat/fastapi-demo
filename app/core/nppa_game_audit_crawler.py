import datetime
import getopt
import logging
import sys

from bs4 import BeautifulSoup
import requests
import re

from sqlalchemy.orm import Session

from app.api import deps
from app.models import EGameAudit, GameRevocationAudit, GameAlterationAudit
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
        self.suffix = ".shtml"

    def __convert_to_soup(self, url: str):
        response = requests.get(url, headers=self.headers)
        response.encoding = "u8"
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def __parse_table(self, url: str) -> list[GameAudit]:
        """Parse data table
        :return: List of game audits
        """
        logging.info(f"Start to parse {url}.")
        soup = self.__convert_to_soup(url)
        ul = soup.find("ul", "m2nrul")
        links = []
        li_list = ul.find_all("li")
        for li in li_list:
            a = li.find("a")
            title = a.text
            url = f"{self.base_url}{a['href']}"
            publish_date = re.sub(r"[\[\]]", "", li.find("span").text)
            links.append(
                GameAudit(
                    title=title,
                    url=url,
                    publish_date=datetime.datetime.strptime(publish_date, "%Y-%m-%d"),
                )
            )
        logging.info("Parse completed.")
        return links

    def __parse_network_game_audits(
        self, url: str, game_type: str
    ) -> list[NetworkGameAudit]:
        """Parse network game audits
        :param url: url of network game
        :param game_type: 320 domestic 318 foreign
        :return: List of network game audits
        """
        logging.info(f"Start to parse network game audit, url: {url}.")
        network_games = []
        soup = self.__convert_to_soup(url)
        # table_rows = []
        table_row_selector = "tr:not([style*=color])"
        if game_type == "320":
            table = soup.find_all("table", class_="trStyle tableNormal")
            table_rows = table[0].select(table_row_selector)
        else:
            table_rows = soup.select(table_row_selector)
        for row in table_rows:
            tds = row.find_all("td")
            td_count = len(tds)
            isbn = "" if td_count == 7 else tds[6].text
            category = 1 if game_type == "320" else 2
            publish_date = tds[6].text if td_count == 7 else tds[7].text
            network_games.append(
                NetworkGameAudit(
                    name=tds[1].text,
                    audit_category=tds[2].text,
                    publisher=tds[3].text,
                    operator=tds[4].text,
                    audit_no=tds[5].text,
                    isbn=isbn,
                    category=category,
                    publish_date=datetime.datetime.strptime(publish_date, "%Y年%m月%d日"),
                )
            )
        logging.info(
            f"Parsed total {len(network_games)} network game audits from url: {url}."
        )
        return network_games

    def __parse_egame_audits(self, url: str) -> list[EGameAudit]:
        """Parse foreign e-game audits
        :param url: url of e-game audits(319)
        :return: List of foreign e-game audits
        """
        logging.info(f"Start to parse e-game audit, url: {url}.")
        egames = []
        soup = self.__convert_to_soup(url)
        table_rows = soup.select("tr:not([style*=color])")
        for row in table_rows:
            tds = row.find_all("td")
            egames.append(
                EGameAudit(
                    name=tds[1].text,
                    publisher=tds[2].text,
                    audit_no=tds[3].text,
                    publish_date=datetime.datetime.strptime(tds[4].text, "%Y年%m月%d日"),
                )
            )

        logging.info(f"Parsed total {len(egames)} e-game audits from url: {url}.")
        return egames

    def __parse_game_revocation_audits(self, url: str) -> list[GameRevocationAudit]:
        """Parse game revocation audits
        :param url: url of revocation 747
        :return: List of game revocation audits
        """
        logging.info(f"Start to parse game audit revocations, url: {url}.")
        revocations = []
        soup = self.__convert_to_soup(url)
        table_rows = soup.select("tr:not([style*=color])")
        for row in table_rows:
            tds = row.find_all("td")
            td_count = len(tds)
            isbn = "" if td_count == 8 else tds[7].text
            approve_date = tds[7].text if td_count == 8 else tds[8].text
            revocations.append(
                GameRevocationAudit(
                    name=tds[1].text,
                    audit_category=tds[2].text,
                    publisher=tds[3].text,
                    operator=tds[4].text,
                    revocation_msg=tds[5].text,
                    audit_no=tds[6].text,
                    isbn=isbn,
                    approval_date=datetime.datetime.strptime(approve_date, "%Y年%m月%d日"),
                )
            )
        logging.info(
            f"Parsed total {len(revocations)} game revocation audits from url: {url}."
        )
        return revocations

    def __parse_game_alteration_audits(self, url: str) -> list[GameAlterationAudit]:
        """Parse game audit changes
        :param url: url of changes(321)
        :return: List of game audit changes
        """
        logging.info(f"Start to parse game change audit, url: {url}.")
        alterations = []
        soup = self.__convert_to_soup(url)
        table_rows = soup.select("tr:not([style*=color])")
        for row in table_rows:
            tds = row.find_all("td")
            td_count = len(tds)
            isbn = "" if td_count == 8 else tds[7].text
            publish_date = tds[7].text if td_count == 8 else tds[8].text
            alterations.append(
                GameAlterationAudit(
                    name=tds[1].text,
                    audit_category=tds[2].text,
                    publisher=tds[3].text,
                    operator=tds[4].text,
                    alteration_msg=tds[5].text,
                    audit_no=tds[6].text,
                    isbn=isbn,
                    alter_date=datetime.datetime.strptime(publish_date, "%Y年%m月%d日"),
                )
            )

        logging.info(
            f"Parsed total {len(alterations)} game change audits from url: {url}."
        )
        return alterations

    def __get_latest_game_audits(self, db: Session) -> None:
        """Get incremental game audits
        :param db: Database session
        """
        links = self.__parse_table(self.base_url + self.data_url + self.suffix)
        latest_date = crud.game_audit.get_latest_date(db)
        links = list(filter(lambda x: x.publish_date > latest_date, links))
        # save links
        if links:
            crud.game_audit.multiple_create(db, objs_in=links)
            logging.info(f"Saved total {len(links)} game audits")
            self.__parse_game_audits(db, links)
        else:
            logging.info("There's no new NPPA game audit to save.")

    def __get_all_game_audits(self, db: Session) -> None:
        """Get full game audits. Will clean up tables and refill data
        :param db: Database session
        """
        is_empty = crud.game_audit.is_empty(db)
        if not is_empty:
            crud.game_audit.delete_all(db)  # clear database table

        soup = self.__convert_to_soup(self.base_url + self.data_url + self.suffix)
        total_page = re.sub(r"\D", "", soup.find("a", class_="sPage_a sPage_prev").text)
        game_audit_list = []
        for i in range(1, int(total_page) + 1):
            current_page = "" if i == 1 else f"_{i}"
            url = f"{self.base_url}{self.data_url}{current_page}{self.suffix}"
            game_audit_list.extend(self.__parse_table(url))
        if game_audit_list:
            crud.game_audit.multiple_create(db, objs_in=game_audit_list)
            logging.info(f"Saved total {len(game_audit_list)} game audits")
            self.__parse_game_audits(db, game_audit_list)
        else:
            logging.info("No NPPA game audit to save.")

    def __parse_game_audits(self, db: Session, game_audits: list[GameAudit]) -> None:
        """Parse game audits
        :param db: Database session
        :param game_audits： List of game audits
        """
        domestic_network_game_cnt = (
            foreign_network_game_cnt
        ) = audit_changes_cnt = audit_cancel_cnt = egame_audit_cnt = 0
        for audits in game_audits:
            data_type = re.search(r"/(\d{3})/", audits.url).group(1)
            if data_type == "318":
                domestic_network_games = self.__parse_network_game_audits(
                    audits.url, data_type
                )
                domestic_network_game_cnt += len(domestic_network_games)
                crud.network_game_audit.multiple_create(
                    db, objs_in=domestic_network_games
                )
                domestic_network_games.clear()
            elif data_type == "320":
                foreign_network_games = self.__parse_network_game_audits(
                    audits.url, data_type
                )
                foreign_network_game_cnt += len(foreign_network_games)
                crud.network_game_audit.multiple_create(
                    db, objs_in=foreign_network_games
                )
                foreign_network_games.clear()
            elif data_type == "321":
                audit_changes = self.__parse_game_alteration_audits(audits.url)
                audit_changes_cnt += len(audit_changes)
                crud.game_alteration_audit.multiple_create(db, objs_in=audit_changes)
                audit_changes.clear()
            elif data_type == "747":
                audit_cancels = self.__parse_game_revocation_audits(audits.url)
                audit_cancel_cnt += len(audit_cancels)
                crud.game_revocation_audit.multiple_create(db, objs_in=audit_cancels)
                audit_cancels.clear()
            elif data_type == "319":
                egames = self.__parse_egame_audits(audits.url)
                egame_audit_cnt += len(egames)
                crud.egame_audit.multiple_create(db, objs_in=egames)
                egames.clear()

        logging.info(f"Saved total {domestic_network_game_cnt} domestic network games.")
        logging.info(f"Saved total {foreign_network_game_cnt} foreign network games.")
        logging.info(f"Saved total {audit_changes_cnt} game audit changes.")
        logging.info(f"Saved total {audit_cancel_cnt} game audit cancels.")
        logging.info(f"Saved total {egame_audit_cnt} foreign e-games.")

    def run(self, mode=0):
        """Entry of the crawler
        :param mode: 0 incremental data 1 full data, default 0
        """
        db: Session = next(deps.get_db())
        if mode == 0:
            self.__get_latest_game_audits(db)
        else:
            self.__get_all_game_audits(db)


def init_log():
    logging.basicConfig(level="INFO")
    logger = logging.getLogger("nppa_game_audit_scraper_logger")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level="DEBUG")
    console_log_format = "%(name)s--->%(asctime)--->%(message)--->%(lineno)d"
    formatter = logging.Formatter(fmt=console_log_format)
    console_handler.setFormatter(fmt=formatter)
    logger.addHandler(console_handler)


def main(argv):
    init_log()
    try:
        opts, args = getopt.getopt(argv, "hm:", ["help", "mode="])
    except getopt.GetoptError:
        print(
            "Error: -m <mode> pr --mode=<mode>, mode is 0 or 1. 0: incremental data, 1: full data"
        )
        sys.exit(2)
    mode = 0
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                "Support parameter mode. e.g: -m <mode> or --mode=<mode>, mode is 0 or 1. 0: incremental data, "
                "1: full data"
            )
            sys.exit()
        elif opt in ("-m", "--mode"):
            arg = int(arg)
            if arg > 1 or arg < 0:
                print("Mode is only supported 0 or 1.")
                sys.exit(2)
            mode = arg
    crawler = NPPAGameAuditCrawler()
    crawler.run(mode)


if __name__ == "__main__":
    main(sys.argv[1:])
