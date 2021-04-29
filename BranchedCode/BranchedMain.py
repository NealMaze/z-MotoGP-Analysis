# import necessary modules
import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
from pprint import pprint
import numpy as np
import pandas as pd


# Headers for all the data we will be scraping in this notebook
headers = ['Year','TRK','Track','Category','Session','Date','Track_Condition','Track_Temp','Air_Temp',
           'Humidity','Position','Points','Rider_Number','Rider_Name','Nationality','Team_Name',
           'Bike','Avg_Speed','Time']

years = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

years = ["2020"]

base_url = 'http://www.motogp.com/en/Results+Statistics/'


# 1) function return a soup object
def soup_special(url):
    """Returns a BeautifulSoup object for the provided url"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# 2) functions to get various datapoints from a soup object
def get_date(soup):
    """ Returns the date of the race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='padbot5')
    if find is None:
        r = 'n/a'
    else:
        r = ','.join(find.text.replace(',',' ').split()[-3:])
    return r

def get_tr_con(soup):
    """ Returns the track condition during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather track_condition')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[2]
    return r

def get_tr_tmp(soup):
    """ Returns the track temperature during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather ground')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[1]
    return r

def get_air_tmp(soup):
    """ Returns the air temperature during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather air')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[1]
    return r

def get_humidity(soup):
    """ Returns the track humidity during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather humidity')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[1]
    return r

def get_all_races(soup):
    """ Returns all the races that took place in a particular season
        for which the soup was passed in """
    find = soup.find(id='event')
    if find is None:
        r = []
    else:
        r = find.find_all('option')
    return r

def get_all_cats(soup):
    """ Returns all the different categories (MotoGP, Moto2, etc.)
        that took place at a particular track in the provided soup """
    find = soup.find(id='category')
    if find is None:
        r = []
    else:
        r = find.find_all('option')
    return r

def get_race_sessions(soup):
    """ Returns all the different race sessions (RACE, RACE2, etc.)
        that took place at a particular track in the provided soup """
    find = soup.find(id='session')
    r = []
    if find is None:
        return r
    else:
        r2 = find.find_all('option')
        for s in r2:
            if s.text.find('RACE') > -1:
                r.append(s.text.replace('E',''))
        return r

# 3) function to get stats about all riders in a specific race
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





years = "2020"

# loop through all parameters

for yr in reversed(years):
    data_list = []
    soup_yr = soup_special(base_url + yr)
    races = get_all_races(soup_yr)
    print(yr)

    for rc in races[0:2]:
        TRK = rc['value']
        Track = rc['title']
        print(TRK, end=", ")
        url_rc = base_url + yr + '/' + TRK + '/'
        soup_rc = soup_special(url_rc)
        categories = get_all_cats(soup_rc)
        print(categories)

        for cat in categories:
            CAT = cat.text
            url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
            soup_c = soup_special(url_c)
            sessions = get_race_sessions(soup_c)
            print("cat")

            for ssn in sessions:
                SSN = ssn
                url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
                print(url_ssn)
#                 soup_ssn = soup_special(url_ssn)
#                 data_list.extend(get_all_stats(soup_ssn, yr, TRK, Track, CAT, SSN))
#                 time.sleep(1 + np.random.random())
#
#     df = pd.DataFrame(data_list, columns=headers)
#     fn = yr + '_data.csv'
#     df.to_csv(fn)
#     print(fn)
#     time.sleep(1 + np.random.random())
#
# print('>> Scraping complete!')

# # first, get all tracks from 2005-2017
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
# def get_GP_info(track_url_str):
#     """
#     Returns a list with track length, number of left corners, number of right corners,
#     track width, and length of longest straight. For any unavailable values, it returns
#     'n/a' instead of a float or int.
#     """
#     url = 'http://www.motogp.com/en/event/' + track_url_str + '#info-track'
#     soupy = soup_special(url)
#     attributes = soupy.find(id='circuit_numbers').find_all(class_='circuit_number_content')
#     strs = []
#     list_data = []
#
#     for s in range(len(attributes)):
#         strs.append(attributes[s].text)
#
#     if float(strs[0].split()[0]) == 0:
#         list_data.append('n/a')
#     else:
#         list_data.append(float(strs[0].split()[0]))
#
#     if strs[1] == '':
#         list_data.append('n/a')
#     else:
#         list_data.append(int(strs[1]))
#
#     if strs[2] == '':
#         list_data.append('n/a')
#     else:
#         list_data.append(int(strs[2]))
#
#     if len(strs[3].split()) == 1:
#         list_data.append('n/a')
#     else:
#         list_data.append(float(strs[3].split()[0]))
#
#     if len(strs[4].split()) == 1:
#         list_data.append('n/a')
#     else:
#         list_data.append(float(strs[4].split()[0]))
#
#     return list_data
#
#
# def get_GP_info_additional(track_url_str):
#     """
#     Returns MotoGP average speed, MotoGP distance, Moto2 distance,
#     and Moto3 distance for the particular track. If data does not exist,
#     it returns 'n/a' in place of a float or int.
#     """
#     url = 'http://www.motogp.com/en/event/' + track_url_str + '#info-track'
#     soupy = soup_special(url)
#
#     # MotoGP average speed
#     avg_speed_str = soupy.find(class_='c-statistics__speed-item').text
#     if avg_speed_str == '-':
#         avg_speed = 'n/a'
#     else:
#         avg_speed = float(avg_speed_str)
#
#     attributes = soupy.find(class_='c-laps__content').find_all(class_='c-laps__item')
#
#     # MotoGP distance
#     GP_dist = float(attributes[9].text.split()[0])
#     if GP_dist == 0: GP_dist = 'n/a'
#
#     # Moto2 distance
#     m2_dist = float(attributes[10].text.split()[0])
#     if m2_dist == 0: m2_dist = 'n/a'
#
#     # Moto3 distance
#     m3_dist = float(attributes[11].text.split()[0])
#     if m3_dist == 0: m3_dist = 'n/a'
#
#     return [avg_speed, GP_dist, m2_dist, m3_dist]
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
#




