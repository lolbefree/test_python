import requests
import sqlite3
import os


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.company = ""
        self.db = "db.sqlite"
        self.conn = sqlite3.connect(self.db)

    def parse_site(self):
        with open(self.filename, "r") as file:
            for line in file:
                line = line.replace("\n", "")
                url = f'https://query1.finance.yahoo.com/v7/finance/download/{line}?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true'
                r = requests.get(url, allow_redirects=True)
                if r:
                    open(f'{os.getcwd()}\\downloads\\{line}.csv', 'wb').write(r.content)
                else:
                    open(f'{os.getcwd()}\\downloads\\{line}_error.csv', 'wb').write(r.content)

    def create_db(self):
        sqlcode = """CREATE TABLE IF NOT EXISTS Company_data (
                                        id integer PRIMARY KEY,
                                        name_ text NOT NULL,
                                        Date_ DATE NOT NULL,
                                        Open_ FLOAT NOT NULL,
                                        High FLOAT NOT NULL,
                                        Low FLOAT NOT NULL,
                                        Close_ FLOAT NOT NULL,
                                        Adj_Close FLOAT NOT NULL,
                                        Volume INTEGER NOT NULL );"""
        cur = self.conn.cursor()
        cur.execute(sqlcode)
        self.conn.commit()

    def insert_in_base(self):
        with open("company_list.txt", "r") as file:
            for row in file:
                row = row.replace("\n", "")
                self.company = row
                try:
                    with open(f"{os.getcwd()}\\downloads\\{row}.csv", "r") as file2:
                        data = file2.readlines()
                        for item in data[1:]:
                            item = item.split(",")

                            sql = f''' INSERT INTO Company_data(name_, Date_ ,Open_ ,High, Low, close_, Adj_Close, Volume)
                                      VALUES('{self.company.upper()}', '{item[0]}', {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}, {item[6]}) '''
                            cur = self.conn.cursor()
                            cur.execute(sql)
                            self.conn.commit()
                except FileNotFoundError:
                    continue

    def main(self):
        self.create_db()
        self.parse_site()
        self.insert_in_base()
        print("END WORK")

Parser("company_list.txt").main()
