import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime
from sqlalchemy import create_engine
import time
import os.path


class Fuel_Info:

    def __init__(self, params, database):
        self.params = params
        self.database = database

    def __write_data_to_DB(self,data):
        ## Write to DB
        # username:password@host:port/database
        engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(self.database["Username"],self.database["password"],self.database["host"],self.database["Database_name"]))
        data.to_sql('stations', con=engine, if_exists='append')

    def __get_datetime_now(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.datum = dt_string
        return dt_string

    def __get_fuel_data(self):
        api_result = requests.get('https://creativecommons.tankerkoenig.de/json/list.php', self.params)
        api_response = api_result.json()
        if api_result.json()['ok']:
            return pd.DataFrame(api_response['stations'])
        else:
            return None

    def generate_db_entry(self):

        while True:
            data = self.__get_fuel_data()
            if data is None:
                print("es gab einen Error mit dem Server")
                with open(os.path.abspath("./error/error.json"),"r+") as file:
                    data = json.load(file)
                    data.update({self.datum:"Daten konnten nicht vom Server abgerufen werden"})
                    file.seek(0)
                    json.dump(data,file)
            else:
                data['date'] = self.__get_datetime_now()
                try:
                    self.__write_data_to_DB(data)
                except:
                    print("es gab einen Error mit der DB")
                    with open(os.path.abspath("./error/error.json"), "r+") as file:
                        data = json.load(file)
                        data.update({self.datum: "Daten konnten nicht in die Datenbank geschrieben werden"})
                        file.seek(0)
                        json.dump(data, file)
            time.sleep(3600)



