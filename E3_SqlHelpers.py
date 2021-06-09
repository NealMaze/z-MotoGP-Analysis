# Imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
from lists import *
from B2_ConverterHelpers import getFileNames

def getEvents(srchCol, srchVal, lge):
    if srchCol == "rdr":
        names = srchVal.split(" ", 1)
        fName = names[0]
        lName = names[1]
        whereState = \
            f"""
            WHERE f_name = {fName}
            AND l_name = {lName};
            """

    elif srchCol == "manu":
        whereState = f"WHERE manu = {srchVal};"

    engine = create_engine("postgresql://postgres:7158@localhost:5432/MotoGP")
    con = engine.connect()

    events = pd.read_sql(
        f"""
        SELECT yr, lge, rnd, session
        FROM gp_times
        {whereState}
        """
    )

    events.drop_duplicates()





