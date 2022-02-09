import plotting_tool
import graphics_processing
import load_data
import processing_ts

metrics = ["engagement", "excitation", "stress", "relax", "interest", "focus"]
colors_metrics = {"engagement": "#BF2F21",
                  "excitation": "#EB9108",
                  "stress": "#C715CD",
                  "relax": "#75602A",
                  "interest": "#2037C6",
                  "focus": "#319B1A"}
dict_colores = {"VL-DNA": "#E8846E",
                "TE-DNA": "#F1E58E",
                "OP-ASSOC": "#8DD47A",
                "OP-PRON": "#A09F90",
                "OP-LIS": "#74BAEE",
                "OP-JOIN": "#4083AF",
                "OP-TRA": "#C574EE",
                "OP-ORD": "#FD95DE",
                "OP-DLG": "#FBA64C"}


def generate_analysis_participant_lesson(root_path_data, id_participant, id_lesson):
    participant_lesson_data_ts = load_data.load_participant_lesson_dataframe(root_path_data,
                                                                             id_participant,
                                                                             id_lesson)
    participant_lesson_time_result = load_data.load_participant_lesson_time_results(root_path_data,
                                                                                    id_participant,
                                                                                    id_lesson)

    data_ts_processed_participant_lesson = processing_ts.process_datetime(participant_lesson_data_ts)
    activities_participant_lesson = processing_ts.process_activities(data_ts_processed_participant_lesson)
    data_time_activity = graphics_processing.generate_data_time_activity(participant_lesson_time_result)
    data_result_lesson_activity = graphics_processing.generate_data_result_activity(participant_lesson_time_result)
    data_time_bar_pie_time_row = graphics_processing.generate_data_time_activity_bar(data_time_activity)
    data_pie_results_row = graphics_processing.generate_data_result_general(data_result_lesson_activity)
    data_bar_results_row = graphics_processing.generate_data_results_activity_bar_grouped(data_result_lesson_activity)

    time_series_row = plotting_tool.generate_time_series_plot(activities_participant_lesson,
                                                              data_ts_processed_participant_lesson,
                                                              metrics,
                                                              colors_metrics,
                                                              dict_colores)

    histogram_row = plotting_tool.generate_row_histogram_metrics(data_ts_processed_participant_lesson,
                                                                 colors_metrics,
                                                                 metrics)

    heatmap_row = plotting_tool.generate_heatmap_row(data_ts_processed_participant_lesson,
                                                     metrics)

    time_row = plotting_tool.generate_row_time(data_time_activity,
                                               data_time_bar_pie_time_row)

    results_row = plotting_tool.generate_row_results(data_result_lesson_activity,
                                                     data_pie_results_row,
                                                     data_bar_results_row)

    rows_graphics_array = [time_series_row, histogram_row, heatmap_row, time_row, results_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()







