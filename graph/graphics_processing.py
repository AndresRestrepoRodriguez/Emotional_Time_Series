import numpy as np
from collections import Counter
import collections, functools, operator


def generate_data_time_activity(json_data):
    array_data = []
    for key in json_data.keys():
        time_value = json_data[key]['time']
        array_data.append([key, time_value])
    return array_data


def generate_data_time_activity_bar(json_data):
    dict_values = {}
    x_values = []
    y_values = []
    for key in json_data.keys():
        if not key == "0-general":
            time_value = json_data[key]['time']
            x_values.append(key)
            y_values.append(time_value)
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    return dict_values


def generate_data_result_activity(json_data):
    array_data = []
    key_results = 'results'
    for key in json_data.keys():
        filter_data = json_data[key]
        if key_results in filter_data:
            results = list(filter_data[key_results].values())
            temp_data = [key] + results
            array_data.append(temp_data)
    return array_data


def generate_data_result_general(data_results_activities):
    dict_values = {}
    name_activity = data_results_activities[0][0]
    x_values = ["Correct", "Incorrect", "Errors / Attempts"]
    y_values = data_results_activities[0][2:]
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    dict_values['name_activity'] = name_activity
    return dict_values


def generate_data_results_activity_bar_grouped(data_results_activities):
    dict_values = {}
    x_values = []
    y_values = []
    name_values = ["Correct", "Incorrect", "Errors / Attempts"]
    for value in data_results_activities[1:]:
        x_values.append(value[0])
        y_values.append(value[2:])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.array(y_values).T.tolist()
    dict_values['name_values'] = name_values
    return dict_values


def get_general_time_lessons(data_json_consolidate):
    time_general_lessons = []
    for key_lesson in data_json_consolidate:
        lesson_time_general_tmp = [key_lesson, data_json_consolidate[key_lesson]['0-general']['time']]
        time_general_lessons.append(lesson_time_general_tmp)
    return time_general_lessons


def get_general_results_lessons(data_json_consolidate):
    array_data = []
    key_results = 'results'
    for key_lesson in data_json_consolidate.keys():
        filter_data = data_json_consolidate[key_lesson]['0-general']
        results = list(filter_data[key_results].values())
        temp_data = [key_lesson] + results
        array_data.append(temp_data)
    return array_data


def generate_data_results_general_lesson_pie(data_general_results_lessons):
    dict_values = {}
    y_values_tmp = []
    x_values = ["Correct", "Incorrect", "Errors / Attempts"]
    for lesson in data_general_results_lessons:
        y_values_tmp.append(lesson[2:])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.sum(y_values_tmp, axis=0)
    return dict_values


def generate_data_results_lessons_bar_grouped(data_results_lessons):
    dict_values = {}
    x_values = []
    y_values = []
    name_values = ["Correct", "Incorrect", "Errors / Attempts"]
    for value in data_results_lessons:
        x_values.append(value[0])
        y_values.append(value[2:])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.array(y_values).T.tolist()
    dict_values['name_values'] = name_values
    return dict_values


def generate_data_time_lessons_bar_pie(time_lesson_processed):
    dict_values = {}
    x_values = []
    y_values = []
    for lesson in time_lesson_processed:
        x_values.append(lesson[0])
        y_values.append(lesson[1])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    return dict_values


def get_metric_all_lessons(df_consolidate_time_series, metric):
    array_metrics_data = []
    for lesson in df_consolidate_time_series.keys():
        array_metrics_data.append(df_consolidate_time_series[lesson][metric])
    return np.concatenate(array_metrics_data).tolist()


def get_metric_all_lessons_consolidate(df_consolidate_time_series, metrics):
    metric_lessons_unified = {}
    for metric in metrics:
        metric_lessons_unified[metric] = get_metric_all_lessons(df_consolidate_time_series, metric)
    return metric_lessons_unified


def get_metric_all_lessons_activity(df_consolidate_time_series, metric):
    array_metrics_data = []
    for lesson in df_consolidate_time_series.keys():
        filter_df_lesson = df_consolidate_time_series[lesson]
        for activity_lesson in filter_df_lesson:
            array_metrics_data.append(activity_lesson[metric])
    return np.concatenate(array_metrics_data).tolist()


def get_metric_all_lessons_activity_consolidate(df_consolidate_time_series, metrics):
    metric_lessons_unified = {}
    for metric in metrics:
        metric_lessons_unified[metric] = get_metric_all_lessons_activity(df_consolidate_time_series, metric)
    return metric_lessons_unified


def get_total_time_lessons_activity(filter_participant_lesson_time_result):
    time_general_lessons_activity = []
    for key_lesson in filter_participant_lesson_time_result.keys():
        lesson_time_general_tmp = [key_lesson, filter_participant_lesson_time_result[key_lesson]]
        time_general_lessons_activity.append(lesson_time_general_tmp)
    return time_general_lessons_activity


def get_results_lessons_activity(data_json_consolidate):
    array_data = []
    for key_lesson in data_json_consolidate.keys():
        filter_data = data_json_consolidate[key_lesson]
        results = list(filter_data.values())
        temp_data = [key_lesson] + results
        array_data.append(temp_data)
    return array_data


def get_metric_all_users(df_consolidate_time_series, metric):
    array_metrics_data = []
    for user_id in df_consolidate_time_series.keys():
        array_metrics_data.append(df_consolidate_time_series[user_id][metric])
    return np.concatenate(array_metrics_data).tolist()


def get_metric_all_group_lessons_consolidate(df_consolidate_time_series, metrics):
    metric_users_unified = {}
    metric_metrics_unified = {}
    for key_id in df_consolidate_time_series.keys():
        filter_user_id_ts = df_consolidate_time_series[key_id]
        metric_users_unified[key_id] = {}
        for metric in metrics:
            metric_users_unified[key_id][metric] = get_metric_all_lessons(filter_user_id_ts, metric)
    for metric in metrics:
        metric_metrics_unified[metric] = get_metric_all_users(metric_users_unified, metric)
    return metric_metrics_unified


def get_summary_group_lessons_time(group_lesson_time_results_json):
    lessons_summary_dict = {}
    for key_user in group_lesson_time_results_json.keys():
        data_user_filter = group_lesson_time_results_json[key_user]
        for key_lesson in data_user_filter:
            data_user_lesson_filter = data_user_filter[key_lesson]
            if not key_lesson in lessons_summary_dict.keys():
                lessons_summary_dict[key_lesson] = {}
            for key_actitity in data_user_lesson_filter:
                if not key_actitity in lessons_summary_dict[key_lesson].keys():
                    lessons_summary_dict[key_lesson][key_actitity] = {}
                    lessons_summary_dict[key_lesson][key_actitity]['time'] = 0
                lessons_summary_dict[key_lesson][key_actitity]['time'] += data_user_lesson_filter[key_actitity]['time']
    return lessons_summary_dict


def get_grouped_group_lessons_results(group_lesson_time_results_json):
    lessons_summary_dict = {}
    for key_user in group_lesson_time_results_json.keys():
        data_user_filter = group_lesson_time_results_json[key_user]
        for key_lesson in data_user_filter:
            data_user_lesson_filter = data_user_filter[key_lesson]
            if not key_lesson in lessons_summary_dict.keys():
                lessons_summary_dict[key_lesson] = {}
            for key_actitity in data_user_lesson_filter:
                if not key_actitity in lessons_summary_dict[key_lesson].keys():
                    lessons_summary_dict[key_lesson][key_actitity] = []
                lessons_summary_dict[key_lesson][key_actitity].append(data_user_lesson_filter[key_actitity]['results'])
    return lessons_summary_dict


class Counter_tweaked(Counter):
    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter_tweaked()
        for elem, count in self.items():
            newcount = count + other[elem]
            result[elem] = newcount
        for elem, count in other.items():
            if elem not in self:
                result[elem] = count
        return result


def get_sum_array_dicts(array_dict):
    result = dict(functools.reduce(operator.add,
                                   map(Counter_tweaked, array_dict)))
    return result


def get_summary_group_lessons_results(grouped_group_lesson_results):
    summary_group_lesson_results = grouped_group_lesson_results.copy()
    for key_lesson in summary_group_lesson_results.keys():
        lesson_filter_data = summary_group_lesson_results[key_lesson]
        for key_actitity in lesson_filter_data.keys():
            array_dict_results = summary_group_lesson_results[key_lesson][key_actitity]
            summary_group_lesson_results[key_lesson][key_actitity] = get_sum_array_dicts(array_dict_results)
    return summary_group_lesson_results


def generate_group_data_time_lesson(summary_group_lesson_time, lesson):
    lesson_str = "lesson_"
    return generate_data_time_activity(summary_group_lesson_time[lesson_str + lesson])


def generate_group_data_time_lesson_bar(summary_group_lesson_time, lesson):
    lesson_str = "lesson_"
    return generate_data_time_activity_bar(summary_group_lesson_time[lesson_str + lesson])


def generate_group_data_results_lesson(summary_group_lesson_results, id_lesson):
    lesson_str = "lesson_"
    array_results = []
    filter_lesson_dict = summary_group_lesson_results[lesson_str + id_lesson]
    for key_activity in filter_lesson_dict:
        results = list(filter_lesson_dict[key_activity].values())
        temp_data = [key_activity] + results
        array_results.append(temp_data)
    return array_results
