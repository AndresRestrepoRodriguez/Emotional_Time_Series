import pandas as pd
import json
import os


ID_PREFIX = "id"
LESSON_PREFIX = "lesson"
UNDERSCORE_VALUE = "_"
DATA_METRICS_FILE_NAME = "data_1secs_extra_exe.csv"


def load_participant_lesson_dataframe(root_path, id_participant, id_lesson):
    path_data_participant_lesson = os.path.join(root_path,
                                                f"{ID_PREFIX}{UNDERSCORE_VALUE}{id_participant}",
                                                f"{LESSON_PREFIX}{UNDERSCORE_VALUE}{id_lesson}",
                                                DATA_METRICS_FILE_NAME)
    metrics_dataframe = pd.read_csv(path_data_participant_lesson)
    return metrics_dataframe


def load_participant_lesson_time_results(root_path, id_participant, id_lesson):
    path_json_participant_lesson = os.path.join(root_path,
                                                f"{ID_PREFIX}{UNDERSCORE_VALUE}{id_participant}",
                                                f"{LESSON_PREFIX}{UNDERSCORE_VALUE}{id_lesson}",
                                                f"results_participant_{id_participant}_lesson_{id_lesson}.json")
    json_data_file_participant_lesson = open(path_json_participant_lesson)
    json_data_participant_lesson = json.load(json_data_file_participant_lesson)
    return json_data_participant_lesson


