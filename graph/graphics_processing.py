import numpy as np


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
    x_values = ["Total Questions", "Correct", "Incorrect", "Errors / Attempts"]
    y_values = data_results_activities[0][1:]
    dict_values['x_values'] = x_values
    dict_values['y_values'] = y_values
    dict_values['name_activity'] = name_activity
    return dict_values


def generate_data_results_activity_bar_grouped(data_results_activities):
    dict_values = {}
    x_values = []
    y_values = []
    name_values = ["Total Questions", "Correct", "Incorrect", "Errors / Attempts"]
    for value in data_results_activities[1:]:
        x_values.append(value[0])
        y_values.append(value[1:])
    dict_values['x_values'] = x_values
    dict_values['y_values'] = np.array(y_values).T.tolist()
    dict_values['name_values'] = name_values
    return dict_values

