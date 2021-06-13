from fuel_package.Fuel_Info import Fuel_Info
import json

if __name__ == "__main__":

    with open("configs/Database.json", "r") as f:
        database = json.load(f)
    f.close()
    with open("configs/params.json", "r") as f:
        params = json.load(f)
    f.close()

    fuel_info = Fuel_Info(params,database)
    fuel_info.generate_db_entry()