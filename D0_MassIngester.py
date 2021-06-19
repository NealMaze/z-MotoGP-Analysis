# Imports
from sqlalchemy import create_engine
import pandas as pd
from lists import *
from B2_ConverterHelpers import *
import psycopg2
from SQL_Strings import *

password = input("\n\nPassword: ")
print("\n\n")

conn = psycopg2.connect(f"host=localhost dbname=postgres user=postgres password={password}")
cur = conn.cursor()

cur.execute(createTimesTable)
conn.commit()

for yr in yrs:
    for lge in lges:
        fLis = getFiles(csvSesDir, f"{yr}-{lge}*.csv")

        if len(fLis) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in fLis:
            with open(file, "r", encoding="utf-8") as f:
                frame = pd.read_csv(f)
                next(frame)



                cur.copy_from(f, "gp_times", sep=",")

conn.commit()



# engine = create_engine("postgresql://postgres:7158@localhost:5432/MotoGP")
#
# for yr in yrs:
#     for lge in lges:
#         fLis = getFiles(csvSesDir, f"{yr}-{lge}*.csv")
#
#         if len(fLis) != 0:
#             print("")
#             print(f" - - - {yr}, {lge} - - - ")
#
#         for file in fLis:
#             with open(file, "r", encoding='utf-8') as f:
#                 df = pd.read_csv(f)
#             df.to_sql("gp_times", con = engine, index = True, index_label = "index", if_exists = "append")
#             print(file)
#
# engine.dispose()
# print("\n\n   - - - data ingested - - -   \n\n")
