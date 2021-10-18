import numpy as np
from lists import *
from B2_ConverterHelpers import getFiles

########################################################################################################################
def construct_average_map(df,  # the full DataFrame
                          parameter,  # in this case, the rider
                          fillCol,  # in this case, the lap/race time
                          ):

    # Here's another way to construct the same thing
    avg_map = {}

    for rider in df[parameter].unique():    # for each unique rider

        # Build a subframe which contains only the information
        # for this rider
        rider_df = df.query(f'{parameter} == {rider}')

        # This builds the average from any non-nan values
        pos = rider_df.iloc[0]

        # This builds a dictionary containing the average
        # for the riders, excluding nan values
        avg_map[rider] = pos


    # The above loops and this dictionary comprehension
    # # should produce the same result
    # avg_map = {parameter: np.nanmean(subdf[fillCol].values)
    #            for (parameter, subdf) in df.groupby(parameter)}

    return avg_map



########################################################################################################################
def actual_or_average(rider,    # the rider of interest
                      value,    # the current time for this lap/race
                      avg_map,  # a dictionary, explained below
                      ):
    # if the value of the time does not exist (is a nan)
    # then pull the average time from the dictionary
    if np.isnan(value):
        return avg_map[rider]

    # if the value of the time exists, don't mess with it
    return value


########################################################################################################################
rnds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "24"]

# for yr in yrs[:1]:
#     for lge in lges[:1]:
#         for rnd in rnds[:1]:
#
#             rndFiles = getFiles(csvFinalDir, f"{yr}-{lge}-Round_{rnd}-*.csv")
#             q2Files = getFiles(csvGridDir, f"{yr}-{lge}-Round_{rnd}-StartGrid.csv")
#
#             if len(rndFiles) == 1: rndFile = rndFiles[0]
#             else: exit("Too many round files")
#
#             if len(q2Files) == 1: q2File = rndFiles[0]
#             else: exit("Too many qualifying files")
#
#             print(rndFile)
#
#             df = pd.read_csv(rndFile)
#             qdf = pd.read_csv(q2File)
#
#             rdrs = df.rdr_num.unique()
#             frames = []
#
#             for rdr in rdrs:
#                 rdrFrame = nf[nf["rdr_num"] == rdr]







#             rider = "rdr_num"
#             col2Fil = "results"
#
#             # This constructs the dictionary to be used
#             avg_map = construct_average_map(df, rider, col2Fil)
#
#             # Here's another way to construct the same result
#             # fixed_values = []
#
#             # This will loop over the rider/time pairs concurrently
#             # for (rider, col2Fil) in zip(df.rider.values, df.col2Fil.values):
#             #
#             #     if np.isnan(col2Fil):    # only fix the nan values
#             #         new_value = avg_map[rider]
#             #     else:                      # otherwise, leave it alone
#             #         new_value = col2Fil
#             #     fixed_values.append(new_value)
#
#             # df[col2Fil] = fixed_values
#
#             # The above statements and this one should be identical
#             df[col2Fil] = [actual_or_average(rider, col2Fil, avg_map)
#                            for (rider, col2Fil) in
#                            zip(df.rider.values, df.col2Fil.values)]
#
#             df.to_csv(f"{rndFile}", index = False)