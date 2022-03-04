import pandas as pd
import numpy as np
import json
import random
from collections import defaultdict


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


def generate_title_complement_group_lesson(id_lesson):
    return f"Group - Lesson: {id_lesson} <br> <b>"


def generate_title_complement_group_lessons( ids_lessons):
    lessons_string = ", ".join(str(id_lesson) for id_lesson in ids_lessons)
    return f"Group - Lessons: {lessons_string} <br> <b>"


def generate_title_complement_group_activity(ids_lessons, activity):
    lessons_string = ", ".join(str(id) for id in ids_lessons)
    return f"Group - Lessons: {lessons_string} - Activity: {activity} <br> <b>"


def generate_random_user_colors(users_ids):
    chars = '0123456789ABCDEF'
    user_str = "user_"
    num_users = len(users_ids)
    users_ids_str = [user_str + user for user in users_ids]
    colors = ['#' + ''.join(random.sample(chars, 6)) for i in range(num_users)]
    users_colors = dict(zip(users_ids_str, colors))
    return users_colors


def concat_list_by_key(list_dict):
    result = defaultdict(list)

    for i in range(len(list_dict)):
        current = list_dict[i]
        for key, value in current.items():
            for j in range(len(value)):
                result[key].append(value[j])
    return result
