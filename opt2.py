from py2opt.routefinder import RouteFinder
import pandas as pd
from tools import sleigh_weight,north_pole,array_haversin,weighted_reindeer_weariness_single_trip,weighted_reindeer_weariness,weighted_trip_length_tuned,get_trips_meta
import numpy as np
from tqdm import tqdm
import random

def opt2(df:pd.DataFrame):
    df_solution = pd.DataFrame()
    # for trip_id in tqdm(df.TripId.unique()):
    for trip_id in tqdm(df.TripId.unique()):
        trip = df[df.TripId == trip_id]
        og_score = weighted_reindeer_weariness_single_trip(trip)
        # trip_rearranged = trip.sort_values("Weight")
        lat = trip.Latitude.to_list()
        lon = trip.Longitude.to_list()
        weight = trip.Weight.to_list()
        g = trip.GiftId.to_list()
        prev_score = weighted_trip_length_tuned(lat,lon,weight)
        for it in range(len(weight)*100):
            rand_idx_1 = random.randint(0, len(g)-1)
            rand_idx_2 = random.randint(0, len(g)-1)
            if rand_idx_1 == rand_idx_2:
                continue
            lat[rand_idx_2], lat[rand_idx_1] = lat[rand_idx_1], lat[rand_idx_2]
            lon[rand_idx_2], lon[rand_idx_1] = lon[rand_idx_1], lon[rand_idx_2]
            weight[rand_idx_2], weight[rand_idx_1] = weight[rand_idx_1], weight[rand_idx_2]
            new_score = weighted_trip_length_tuned(lat,lon,weight)
            if prev_score > new_score:
                prev_score = new_score
                g[rand_idx_2], g[rand_idx_1] = g[rand_idx_1], g[rand_idx_2]
            else:
                lat[rand_idx_2], lat[rand_idx_1] = lat[rand_idx_1], lat[rand_idx_2]
                lon[rand_idx_2], lon[rand_idx_1] = lon[rand_idx_1], lon[rand_idx_2]
                weight[rand_idx_2], weight[rand_idx_1] = weight[rand_idx_1], weight[rand_idx_2]

        trip_rearranged = trip.set_index('GiftId').loc[g].reset_index()
        if og_score>weighted_reindeer_weariness_single_trip(trip_rearranged):
            df_solution = pd.concat([df_solution,trip_rearranged])
        else:
            df_solution = pd.concat([df_solution,trip])
    return df_solution.set_index('GiftId').reset_index()
    # print(f"og  :{weighted_reindeer_weariness(df):20.0f}")
    # print(f"new :{weighted_reindeer_weariness(df_solution):20.0f}")
opt2("data/trips_combined.csv").to_csv("data/opt3.csv")
print(weighted_reindeer_weariness(pd.read_csv("data/opt2.csv",index_col= 0)))
# print(weighted_reindeer_weariness(opt2(pd.read_csv("data/trips_to_giftsr_random.csv",index_col= 0))))
# print(weighted_reindeer_weariness(opt2(pd.read_csv("data/trips_combined.csv",index_col= 0))))

