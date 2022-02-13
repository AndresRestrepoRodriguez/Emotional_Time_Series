from .graph import graphics_processing, plotting_tool
from .timeseries import processing_ts, load_data

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

colors_lessons = dict(lesson_1="#E8846E", lesson_2="#F1E58E", lesson_3="#8DD47A", lesson_4="#A09F90")


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
    data_time_bar_pie_time_row = graphics_processing.generate_data_time_activity_bar(participant_lesson_time_result)
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


def generate_analysis_participant_lessons(root_path_data, id_participant, ids_lessons):
    participant_lessons_data_ts = load_data.load_participant_lessons_consolidate(root_path_data,
                                                                                 id_participant,
                                                                                 ids_lessons)

    participant_lesson_time_result = load_data.load_results_participant_lessons_consolidate(root_path_data,
                                                                                            id_participant,
                                                                                            ids_lessons)

    processed_participant_lessons_data_ts = processing_ts.process_datetime_lessons(participant_lessons_data_ts)

    time_general_lessons = graphics_processing.get_general_time_lessons(participant_lesson_time_result)
    time_lessons_bar = graphics_processing.generate_data_time_lessons_bar_pie(time_general_lessons)
    results_processed_lessons_general = graphics_processing.get_general_results_lessons(participant_lesson_time_result)
    data_results_general_lesson_pie = graphics_processing.generate_data_results_general_lesson_pie(
        results_processed_lessons_general)
    data_results_lessons_bar_grouped = graphics_processing.generate_data_results_lessons_bar_grouped(
        results_processed_lessons_general)
    consolidate_metrics_lessons_unified = graphics_processing.get_metric_all_lessons_consolidate(
        processed_participant_lessons_data_ts,
        metrics)
    most_long_time_serie_key = processing_ts.get_most_long_time_series(processed_participant_lessons_data_ts)
    most_long_time_serie_data_ts = processed_participant_lessons_data_ts[most_long_time_serie_key]

    time_series_group_row = plotting_tool.generate_time_series_partipant_metrics(processed_participant_lessons_data_ts,
                                                                                 metrics,
                                                                                 most_long_time_serie_data_ts,
                                                                                 colors_lessons)

    histograms_unified_row = plotting_tool.generate_row_histogram_metrics_lessons_unified(
        consolidate_metrics_lessons_unified,
        colors_metrics,
        metrics)

    histograms_overlayed_row = plotting_tool.generate_row_histogram_metrics_lessons_overlay(
        consolidate_metrics_lessons_unified,
        colors_lessons,
        metrics)

    heatmaps_row = plotting_tool.generate_heatmap_row_lessons_overlay(processed_participant_lessons_data_ts, metrics)

    time_row = plotting_tool.generate_row_time_participant_lessons(time_general_lessons, time_lessons_bar)

    results_row = plotting_tool.generate_row_results(results_processed_lessons_general,
                                                     data_results_general_lesson_pie,
                                                     data_results_lessons_bar_grouped)

    rows_graphics_array = [time_series_group_row, histograms_unified_row, histograms_overlayed_row,
                           heatmaps_row, time_row, results_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()
