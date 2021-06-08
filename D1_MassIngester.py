from sqlalchemy import create_engine
import pandas as pd
from lists import *
from B2_ConverterHelpers import getFileNames

engine = create_engine("postgresql://postgres:7158@localhost:5432/MotoGP")

for yr in yrs:
    for lge in lges:
        fLis = getFileNames(csvDir, f"{yr}-{lge}*.csv")

        if len(fLis) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in fLis:
            with open(file, "r", encoding='utf-8') as f:
                df = pd.read_csv(f)
            df.to_sql("gp_times", con = engine, index = False, if_exists = "replace")
            print(file)
