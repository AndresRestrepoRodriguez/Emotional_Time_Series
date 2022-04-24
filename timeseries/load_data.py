import pandas as pd
import json
import os

ID_PREFIX = "id"
LESSON_PREFIX = "lesson"
UNDERSCORE_VALUE = "_"
DATA_METRICS_FILE_NAME = "emotional_data.csv"
RESULTS_TIME_FILE_NAME = "results_time.json"


def load_participant_lesson_dataframe(root_path, id_participant, id_lesson):
    path_data_participant_lesson = os.path.join(root_path,
                                                f"{ID_PREFIX}{UNDERSCORE_VALUE}{id_participant}",
                                                f"{LESSON_PREFIX}{UNDERSCORE_VALUE}{id_lesson}",
                                                DATA_METRICS_FILE_NAME)
    metrics_dataframe = pd.read_csv(path_data_participant_lesson, keep_default_na=False)
    return metrics_dataframe


def load_participant_lesson_time_results(root_path, id_participant, id_lesson):
    path_json_participant_lesson = os.path.join(root_path,
                                                f"{ID_PREFIX}{UNDERSCORE_VALUE}{id_participant}",
                                                f"{LESSON_PREFIX}{UNDERSCORE_VALUE}{id_lesson}",
                                                RESULTS_TIME_FILE_NAME)
    json_data_file_participant_lesson = open(path_json_participant_lesson)
    json_data_participant_lesson = json.load(json_data_file_participant_lesson)
    return json_data_participant_lesson


def load_participant_lessons_consolidate(root_path, id_participant, id_lessons):
    lesson_str = "lesson_"
    dict_lessons = {}
    for lesson in id_lessons:
        data_tmp = load_participant_lesson_dataframe(root_path, id_participant, lesson)
        # data_tmp_processed = process_datetime(data_tmp)
        dict_lessons[lesson_str + lesson] = data_tmp
    return dict_lessons


def load_results_participant_lessons_consolidate(root_path, id_participant, id_lessons):
    lesson_str = "lesson_"
    dict_lessons_results = {}
    for lesson in id_lessons:
        data_tmp = load_participant_lesson_time_results(root_path, id_participant, lesson)
        dict_lessons_results[lesson_str + lesson] = data_tmp
    return dict_lessons_results


def load_group_lesson_consolidate(root_path, id_participants, id_lesson):
    lesson_str = "lesson_"
    user_str = "user_"
    dict_group_lesson = {}
    for id_participant in id_participants:
        dict_group_lesson[user_str + id_participant] = {
            lesson_str + id_lesson: load_participant_lesson_dataframe(root_path, id_participant, id_lesson)}
    return dict_group_lesson


def load_results_group_lesson(root_path, id_participants, id_lesson):
    lesson_str = "lesson_"
    user_str = "user_"
    dict_group_lesson = {}
    for id_participant in id_participants:
        dict_group_lesson[user_str + id_participant] = {
            lesson_str + id_lesson: load_participant_lesson_time_results(root_path, id_participant,
                                                                         id_lesson)}
    return dict_group_lesson


def load_group_lessons_consolidate(root_path, id_participants, id_lessons):
    lesson_str = "lesson_"
    user_str = "user_"
    dict_group_lesson = {}
    for id_participant in id_participants:
        dict_group_lesson[user_str + id_participant] = {}
        for id_lesson in id_lessons:
            dict_group_lesson[user_str + id_participant][
                lesson_str + id_lesson] = load_participant_lesson_dataframe(root_path, id_participant, id_lesson)
    return dict_group_lesson


def load_results_group_lessons(root_path, id_participants, id_lessons):
    lesson_str = "lesson_"
    user_str = "user_"
    dict_group_lesson = {}
    for id_participant in id_participants:
        dict_group_lesson[user_str + id_participant] = {}
        for id_lesson in id_lessons:
            dict_group_lesson[user_str + id_participant][lesson_str + id_lesson] = \
                load_participant_lesson_time_results(root_path, id_participant, id_lesson)
    return dict_group_lesson
