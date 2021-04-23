"""
example URLs
baseUrl = https://www.motogp.com/en/Results+Statistics/
url_yr = https://www.motogp.com/en/Results+Statistics/2020
url_rc = https://www.motogp.com/en/Results+Statistics/2020/QAT/
url_c = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/
url_ssn = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/FP1/Classification
"""

# import necessary modules
from pdfHelpers import *


# Headers for all the data we will be scraping in this notebook
headers = ['Year','TRK','Track','Category','Session','Date','Track_Condition','Track_Temp','Air_Temp',
           'Humidity','Position','Points','Rider_Number','Rider_Name','Nationality','Team_Name',
           'Bike','Avg_Speed','Time']

# indepth analysis is only available as far back as 1998
yearsFull = ["2021", "2020", "2019", "2018", "2017", '2016', '2015', "2014", '2013', '2012', '2011', '2010', '2009', '2008',
         '2007', '2006','2005', "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

years = ["2016"]

allOffSeasonLinks = []

base_url = 'http://www.motogp.com/en/Results+Statistics/'

# 1) function to get stats about all riders in a specific race
def get_all_stats(soup, year, trk, track, cat, ssn):
    if soup.find('tbody') is None:
        return [dict(zip(headers, [year, trk, track, cat, ssn] + ['n/a'] * (len(headers) - 3)))]
    else:
        riders = soup.find('tbody').find_all('a')
        stats_to_return = []

        # raceday stats
        date = get_date(soup)
        tr_con = get_tr_con(soup)
        tr_tmp = get_tr_tmp(soup)
        air_tmp = get_air_tmp(soup)
        humid = get_humidity(soup)

        # rider stats
        for r in riders:
            if ssn == "RACE":
                pos = r.findPrevious().findPrevious().findPrevious().findPrevious().text
                if pos == '':
                    pos = 'crash'
                else:
                    pos = int(pos)
                points = r.findPrevious().findPrevious().findPrevious().text
                if points == '':
                    points = 0
                else:
                    points = float(points)
            else:
                pos = None
                points = None
            r_num = r.findPrevious().findPrevious().text
            if r_num != '':
                r_num = int(r_num)
            r_nam = r.text
            r_nat = r.findNext().text
            team = r.findNext().findNext().text
            bike = r.findNext().findNext().findNext().text
            avgspd = r.findNext().findNext().findNext().findNext().text
            time = r.findNext().findNext().findNext().findNext().findNext().text

            stats_dict = dict(zip(headers, [year, trk, track, cat, ssn, date, tr_con, tr_tmp, air_tmp,
                                            humid, pos, points, r_num, r_nam, r_nat, team,
                                            bike, avgspd, time]))
            stats_to_return.append(stats_dict)
            return stats_to_return

for yr in years:
    fileNum = 0
    # data_list = []
    url_yr = base_url + yr
    soupYr = soup_special(url_yr)
    weekends = get_all_races(soupYr)
    print(f"\nyr")
    #tests = getAllTests(soupYr, yr)
    #
    # for tst in tests[0 : 1]:
    #     x = 1

    for wk in weekends[0 : 1]:
        TRK = wk['value']
        Track = wk['title']
        urlWk = base_url + yr + '/' + TRK + '/'
        soupWk = soup_special(urlWk)
        categories = get_all_cats(soupWk)

        for cat in categories[0 : 1]:
            CAT = cat.text
            url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
            soup_c = soup_special(url_c)
            sessions = get_all_sessions(soup_c)

            for ssn in sessions:
                fName = f"{yr}-{fileNum}{CAT}_{TRK}_{ssn}"
                SSN = ssn
                url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
                soupSSN = soup_special(url_ssn)
                # data_list.extend(get_all_stats(soup_ssn, yr, TRK, Track, CAT, SSN)) ##################################
                pdfLinks = getPDFs(soupSSN, yr)
                for link in pdfLinks:
                    pdf = requests.get(link)
                    with open(f"{fName}.pdf", "wb") as f:
                        f.write(pdf.content)
                time.sleep(1 + np.random.random())
                fileNum += 1
#




#     df = pd.DataFrame(data_list, columns=headers)
#     fn = yr + '_data.csv'
#     df.to_csv(fn)
#     print(fn)
#     time.sleep(1 + np.random.random())
#
# print('>> Scraping complete!')

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

# # first, get all tracks from years
# track_list = []
# GPs_list = []
# track_names = []
#
# for yr in reversed(years):
#     soup_yr = soup_special(base_url + yr)
#     races = get_all_races(soup_yr)
#     print('')
#     print(yr, end=" - ")
#
#     for rc in races:
#         TRK = rc['value']
#         Track = rc['title']
#         print(TRK, end=", ")
#         track_list.append(TRK)
#         GPs_list.append(Track.split(' - ')[0])
#         track_names.append(Track.split(' - ')[1])
#
#     time.sleep(1 + np.random.random())
#
# # extract the unique ones
# combined_list = []
# for index, item in enumerate(track_list):
#     combined_list.append(item+' - '+track_names[index])
# combined_track_set = set(combined_list)
#
# track_url_dict = {'AME - Circuit Of The Americas':'Americas',
#                   'ARA - MotorLand Aragón':'Aragon',
#                   'ARG - Termas de Río Hondo':'Argentina',
#                   'AUS - Phillip Island':'Australia',
#                   'AUT - Red Bull Ring – Spielberg':'Austria',
#                   'CAT - Circuit de Barcelona-Catalunya':'Catalunya',
#                   'CHN - Shanghai Circuit':0,
#                   'CZE - Automotodrom Brno':'Czech+Republic',
#                   'FRA - Le Mans':'France',
#                   'GBR - Donington Park Circuit':0,
#                   'GBR - Silverstone Circuit':'Great+Britain',
#                   'GER - Sachsenring':'Germany',
#                   'INP - Indianapolis Motor Speedway':0,
#                   'ITA - Autodromo del Mugello':'Italy',
#                   'JPN - Twin Ring Motegi':'Japan',
#                   'MAL - Sepang International Circuit':'Malaysia',
#                   'NED - TT Circuit Assen':'Netherlands',
#                   'POR - Estoril Circuit':0,
#                   'QAT - Losail International Circuit':'Qatar',
#                   'RSM - Misano World Circuit Marco Simoncelli':'San+Marino',
#                   'SPA - Circuito de Jerez':'Spain',
#                   'TUR - Istanbul Circuit':0,
#                   'USA - Mazda Raceway Laguna Seca':0,
#                   'VAL - Circuit Ricardo Tormo':'Valencia'}
#
# # functions to get basic track info
#
#
#
#
#
# # make a list of dictionaries for track information
# headers_2 = ['GP','track_length_km','l_corners','r_corners',
#            'width_m','straight_m','GP_avg_speed','gp_dist',
#            'm2_dist','m3_dist']
#
# track_data = []
# for track in combined_track_set:
#     if track_url_dict[track] != 0:
#         print('//', end='')
#         l_GP, L_c, R_c, wid, strt = get_GP_info(track_url_dict[track])
#         GP_avg_spd, gp_d, m2_d, m3_d = get_GP_info_additional(track_url_dict[track])
#         track_dict = dict(zip(headers, [track,l_GP,L_c,R_c,wid,strt,GP_avg_spd,gp_d,m2_d,m3_d]))
#         track_data.append(track_dict)
#         time.sleep(1+np.random.random())
# print('Complete!')
#
# # manually add in the info for tracks which have a 0 in the track_url_dict
# # information is from archived PDFs like the one at this following link
# # http://resources.motogp.com/files/results/2006/CHN/circuit+information.pdf?v1_96143780
#
# dict_shanghai = {'GP': 'CHN - Shanghai Circuit','GP_avg_speed': 'n/a','gp_dist': 'n/a',
#                  'l_corners': 7,'m2_dist': 'n/a','m3_dist': 'n/a','r_corners': 7,
#                  'straight_m': 1202.0,'track_length_km': 5.281,'width_m': 14.0}
#
# dict_donington = {'GP': 'GBR - Donington Park Circuit','GP_avg_speed': 'n/a','gp_dist': 'n/a',
#                   'l_corners': 4,'m2_dist': 'n/a','m3_dist': 'n/a','r_corners': 7,
#                   'straight_m': 564.0,'track_length_km': 4.023,'width_m': 10.0}
#
# dict_indianapolis = {'GP': 'INP - Indianapolis Motor Speedway','GP_avg_speed': 'n/a','gp_dist': 'n/a',
#                      'l_corners': 10,'m2_dist': 'n/a','m3_dist': 'n/a','r_corners': 6,
#                      'straight_m': 644.0,'track_length_km': 4.216,'width_m': 16.0}
#
# dict_estoril = {'GP': 'POR - Estoril Circuit','GP_avg_speed': 'n/a','gp_dist': 'n/a',
#                 'l_corners': 4,'m2_dist': 'n/a','m3_dist': 'n/a','r_corners': 9,
#                 'straight_m': 986.0,'track_length_km': 4.182,'width_m': 14.0}
#
# dict_istanbul = {'GP': 'TUR - Istanbul Circuit','GP_avg_speed': 'n/a','gp_dist': 'n/a',
#                  'l_corners': 8,'m2_dist': 'n/a','m3_dist': 'n/a','r_corners': 6,
#                  'straight_m': 720.0,'track_length_km': 5.340,'width_m': 21.0}
#
# dict_laguna = {'GP': 'USA - Mazda Raceway Laguna Seca','GP_avg_speed': 'n/a','gp_dist': 'n/a',
#                   'l_corners': 7,'m2_dist': 'n/a','m3_dist': 'n/a','r_corners': 4,
#                   'straight_m': 966.0,'track_length_km': 3.610,'width_m': 15.0}
#
# track_data.append(dict_shanghai)
# track_data.append(dict_donington)
# track_data.append(dict_indianapolis)
# track_data.append(dict_estoril)
# track_data.append(dict_istanbul)
# track_data.append(dict_laguna)
#
# # save to CSV
# df_tracks = pd.DataFrame(track_data, columns=headers_2)
# fn = 'Racetrack_data.csv'
# df_tracks.to_csv(fn)
# print(fn)
