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


def generate_title_complement_user_lesson(id_user, id_lesson):
    return f"User: {id_user} - Lesson: {id_lesson} <br> <b>"


def generate_title_complement_user_lessons(id_user, ids_lessons):
    lessons_string = ", ".join(str(id) for id in ids_lessons)
    return f"User: {id_user} - Lessons: {lessons_string} <br> <b>"


def generate_title_complement_user_activity(id_user, ids_lessons, activity):
    lessons_string = ", ".join(str(id) for id in ids_lessons)
    return f"User: {id_user} - Lessons: {lessons_string} - Activity: {activity} <br> <b>"


def generate_title_complement_user_subactivity(id_user, ids_lessons, activity, sub_activity):
    lessons_string = ", ".join(str(id) for id in ids_lessons)
    return f"User: {id_user} - Lessons: {lessons_string} - Activity: {activity} - Sub Activity: {sub_activity} <br> <b>"
