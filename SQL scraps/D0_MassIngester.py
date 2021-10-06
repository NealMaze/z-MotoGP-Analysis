# Imports
from sqlalchemy import create_engine
import pandas as pd
from lists import *
from B2_ConverterHelpers import *
import psycopg2
import numpy
from SQL_Strings import *

password = input("\n\nPassword: ")
print("\n\n")

engine = create_engine("postgresql://postgres:7158@localhost:5432/MotoGP")
conn = psycopg2.connect(f"host=localhost dbname=MotoGP user=postgres password={password}")
cur = conn.cursor()

cur.execute(dropTimesTable)
conn.commit()
cur.execute(createTimesTable)
conn.commit()

for yr in yrs:
    for lge in lges:
        fLis = getFiles(csvSesDir, f"{yr}-{lge}*.csv")

        if len(fLis) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in fLis:
            print(file)
            with open(file, "r", encoding="utf-8") as f:
                # reader = csv.reader(f, delimiter = ",")
                # x = list(reader)
                # result = numpy.array(x).astype("str")
                # for row in result:
                #     print(row)

                df = pd.read_csv(f)
                df.to_sql("gp_times", con = engine, if_exists = "append", index = False)

                # conn.commit()
                # frame = pd.read_csv(f)
                # next(frame)
                # cur.copy_from(f, "gp_times", sep=",")




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
