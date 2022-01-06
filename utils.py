import pandas as pd
import numpy as np
import json


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


def save_dict_as_json(dict_data, path_to_save):
  file_json = open(path_to_save, "w")
  json.dump(dict_data, file_json, default=np_encoder, indent=4)
  

def read_csv_as_dataframe(path_csv):
    return pd.read_csv(path_csv)

