from .graph import graphics_processing, plotting_tool
from .timeseries import processing_ts, load_data, utils

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

    complementary_title = utils.generate_title_complement_user_lesson(id_participant, id_lesson)

    time_series_row = plotting_tool.generate_time_series_plot(activities_participant_lesson,
                                                              data_ts_processed_participant_lesson,
                                                              metrics,
                                                              colors_metrics,
                                                              dict_colores,
                                                              complementary_title)

    histogram_row = plotting_tool.generate_row_histogram_metrics(data_ts_processed_participant_lesson,
                                                                 colors_metrics,
                                                                 metrics,
                                                                 complementary_title)

    heatmap_row = plotting_tool.generate_heatmap_row(data_ts_processed_participant_lesson,
                                                     metrics,
                                                     complementary_title)

    time_row = plotting_tool.generate_row_time(data_time_activity,
                                               data_time_bar_pie_time_row,
                                               complementary_title)

    results_row = plotting_tool.generate_row_results(data_result_lesson_activity,
                                                     data_pie_results_row,
                                                     data_bar_results_row,
                                                     complementary_title)

    rows_graphics_array = [time_series_row, histogram_row, heatmap_row, time_row, results_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()
        print("\n\n")


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

    complementary_title = utils.generate_title_complement_user_lessons(id_participant, ids_lessons)

    time_series_group_row = plotting_tool.generate_time_series_partipant_metrics(processed_participant_lessons_data_ts,
                                                                                 metrics,
                                                                                 most_long_time_serie_data_ts,
                                                                                 colors_lessons,
                                                                                 complementary_title)

    histograms_unified_row = plotting_tool.generate_row_histogram_metrics_lessons_unified(
        consolidate_metrics_lessons_unified,
        colors_metrics,
        metrics,
        complementary_title)

    histograms_overlayed_row = plotting_tool.generate_row_histogram_metrics_lessons_overlay(
        processed_participant_lessons_data_ts,
        colors_lessons,
        metrics,
        complementary_title)

    heatmaps_row = plotting_tool.generate_heatmap_row_lessons_overlay(processed_participant_lessons_data_ts, metrics,
                                                                      complementary_title)

    time_row = plotting_tool.generate_row_time_participant_lessons(time_general_lessons, time_lessons_bar,
                                                                   complementary_title)

    results_row = plotting_tool.generate_row_results_participant_lessons(results_processed_lessons_general,
                                                                         data_results_general_lesson_pie,
                                                                         data_results_lessons_bar_grouped,
                                                                         complementary_title)

    rows_graphics_array = [time_series_group_row, histograms_unified_row, histograms_overlayed_row,
                           heatmaps_row, time_row, results_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()
        print("\n\n")


def generate_analysis_participant_lessons_activity(root_path_data, id_participant, ids_lessons, activity_info):
    participant_lessons_data_ts = load_data.load_participant_lessons_consolidate(root_path_data,
                                                                                 id_participant,
                                                                                 ids_lessons)
    participant_activity_lessons_data_ts = processing_ts.get_participant_lessons_activity(participant_lessons_data_ts,
                                                                                          activity_info)
    participant_activity_lessons_data_ts_processed = processing_ts.process_datetime_lessons_activity(
        participant_activity_lessons_data_ts)
    participant_activity_lessons_data_ts_processed_reset = processing_ts.reset_datetime_index_lessons_activity(
        participant_activity_lessons_data_ts_processed)

    participant_lesson_time_result = load_data.load_results_participant_lessons_consolidate(root_path_data,
                                                                                            id_participant,
                                                                                            ids_lessons)
    participant_lesson_time_activity_result = processing_ts.filter_participant_lesson_time_result(
        participant_lesson_time_result,
        activity_info)

    consolidate_metrics_lessons_unified = graphics_processing.get_metric_all_lessons_activity_consolidate(
        participant_activity_lessons_data_ts_processed_reset, metrics)

    time_lesson_activity = graphics_processing.get_total_time_lessons_activity(participant_lesson_time_activity_result)
    time_lesson_activity_bar_pie = graphics_processing.generate_data_time_lessons_bar_pie(time_lesson_activity)

    participant_lesson_activity_results = processing_ts.filter_participant_lesson_results(
        participant_lesson_time_result, activity_info)
    participant_lesson_activity_results = graphics_processing.get_results_lessons_activity(
        participant_lesson_activity_results)
    participant_lesson_activity_results_pie = graphics_processing.generate_data_results_general_lesson_pie(
        participant_lesson_activity_results)
    participant_lesson_activity_results_bar = graphics_processing.generate_data_results_lessons_bar_grouped(
        participant_lesson_activity_results)

    complementary_title = utils.generate_title_complement_user_activity(id_participant,
                                                                        ids_lessons,
                                                                        activity_info)

    time_series_group_activity_row = plotting_tool.generate_time_series_partipant_lesson_activity_metrics(
        participant_activity_lessons_data_ts_processed_reset, metrics, colors_lessons, complementary_title)

    histograms_unified_activity_row = plotting_tool.generate_row_histogram_metrics_lessons_activity_unified(
        consolidate_metrics_lessons_unified, colors_metrics, metrics, complementary_title)

    histograms_overlayed_activity_row = plotting_tool.generate_row_histogram_metrics_lessons_activity_overlay(
        participant_activity_lessons_data_ts_processed_reset, colors_lessons, metrics, complementary_title)

    heatmaps_activity_row = plotting_tool.generate_heatmap_row_lesson_activity_overlay(
        participant_activity_lessons_data_ts_processed_reset, metrics, complementary_title)

    time_activity_row = plotting_tool.generate_row_time_participant_lessons_activity(time_lesson_activity,
                                                                                     time_lesson_activity_bar_pie,
                                                                                     complementary_title)

    results_activity_row = plotting_tool.generate_row_results_participant_lesson_activity(
        participant_lesson_activity_results,
        participant_lesson_activity_results_pie,
        participant_lesson_activity_results_bar,
        complementary_title)

    rows_graphics_array = [time_series_group_activity_row,
                           histograms_unified_activity_row,
                           histograms_overlayed_activity_row,
                           heatmaps_activity_row,
                           time_activity_row,
                           results_activity_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()
        print("\n\n")


def generate_analysis_participant_lessons_subactivity(root_path_data, id_participant, ids_lessons, activity_info,
                                                      sub_activity):
    participant_lessons_data_ts = load_data.load_participant_lessons_consolidate(root_path_data,
                                                                                 id_participant,
                                                                                 ids_lessons)
    participant_subactivity_lessons_data_ts = processing_ts.get_participant_lessons_subactivity(
        participant_lessons_data_ts,
        activity_info,
        sub_activity)

    participant_subactivity_lessons_data_ts_processed = processing_ts.process_datetime_lessons_activity(
        participant_subactivity_lessons_data_ts)
    participant_subactivity_lessons_data_ts_processed_reset = processing_ts.reset_datetime_index_lessons_activity(
        participant_subactivity_lessons_data_ts_processed)

    participant_lesson_time_result = load_data.load_results_participant_lessons_consolidate(root_path_data,
                                                                                            id_participant,
                                                                                            ids_lessons)
    participant_lesson_time_subactivity_result = processing_ts.filter_participant_lesson_subactivity_time_result(
        participant_lesson_time_result,
        activity_info,
        sub_activity)

    consolidate_metrics_lessons_unified = graphics_processing.get_metric_all_lessons_activity_consolidate(
        participant_subactivity_lessons_data_ts_processed_reset, metrics)

    time_lesson_subactivity = graphics_processing.get_total_time_lessons_activity(
        participant_lesson_time_subactivity_result)
    time_lesson_subactivity_bar_pie = graphics_processing.generate_data_time_lessons_bar_pie(time_lesson_subactivity)

    participant_lesson_subactivity_results = processing_ts.filter_participant_lesson_subactivity_results(
        participant_lesson_time_result, activity_info, sub_activity)
    participant_lesson_subactivity_results = graphics_processing.get_results_lessons_activity(
        participant_lesson_subactivity_results)
    participant_lesson_subactivity_results_pie = graphics_processing.generate_data_results_general_lesson_pie(
        participant_lesson_subactivity_results)
    participant_lesson_subactivity_results_bar = graphics_processing.generate_data_results_lessons_bar_grouped(
        participant_lesson_subactivity_results)

    complementary_title = utils.generate_title_complement_user_subactivity(id_participant,
                                                                           ids_lessons,
                                                                           activity_info,
                                                                           sub_activity)

    time_series_group_subactivity_row = plotting_tool.generate_time_series_partipant_lesson_activity_metrics(
        participant_subactivity_lessons_data_ts_processed_reset, metrics, colors_lessons, complementary_title)

    histograms_unified_subactivity_row = plotting_tool.generate_row_histogram_metrics_lessons_activity_unified(
        consolidate_metrics_lessons_unified, colors_metrics, metrics, complementary_title)

    histograms_overlayed_subactivity_row = plotting_tool.generate_row_histogram_metrics_lessons_activity_overlay(
        participant_subactivity_lessons_data_ts_processed_reset, colors_lessons, metrics, complementary_title)

    heatmaps_subactivity_row = plotting_tool.generate_heatmap_row_lesson_activity_overlay(
        participant_subactivity_lessons_data_ts_processed_reset, metrics, complementary_title)

    time_subactivity_row = plotting_tool.generate_row_time_participant_lessons_activity(time_lesson_subactivity,
                                                                                        time_lesson_subactivity_bar_pie,
                                                                                        complementary_title)

    results_subactivity_row = plotting_tool.generate_row_results_participant_lesson_activity(
        participant_lesson_subactivity_results,
        participant_lesson_subactivity_results_pie,
        participant_lesson_subactivity_results_bar,
        complementary_title)

    rows_graphics_array = [time_series_group_subactivity_row,
                           histograms_unified_subactivity_row,
                           histograms_overlayed_subactivity_row,
                           heatmaps_subactivity_row,
                           time_subactivity_row,
                           results_subactivity_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()
        print("\n\n")


def generate_analysis_participant_lessons_subactivity(root_path_data, ids_group, id_lesson):
    group_lesson_data_ts = load_data.load_group_lesson_consolidate(root_path_data, ids_group, id_lesson)
    group_lesson_data_ts_processed = processing_ts.process_datatime_group_lesson(group_lesson_data_ts)
    group_lesson_time_results = load_data.load_results_group_lesson(root_path_data, ids_group, id_lesson)

    users_colors = utils.generate_random_user_colors(ids_group)
    user_id_max_ts_key, lesson_user_max_ts_key = processing_ts.get_most_long_time_series_group(
        group_lesson_data_ts_processed)
    most_long_time_serie_data_ts = group_lesson_data_ts_processed[user_id_max_ts_key][lesson_user_max_ts_key]
    complementary_title = utils.generate_title_complement_group_lesson(id_lesson)

    consolidate_metrics_group_unified = graphics_processing.get_metric_all_group_lessons_consolidate(
        group_lesson_data_ts_processed, metrics)

    summary_group_lesson_time = graphics_processing.get_summary_group_lessons_time(group_lesson_time_results)
    grouped_group_lesson_results = graphics_processing.get_grouped_group_lessons_results(group_lesson_time_results)
    summary_group_lesson_results = graphics_processing.get_summary_group_lessons_results(grouped_group_lesson_results)

    group_data_time_lesson = graphics_processing.generate_group_data_time_lesson(summary_group_lesson_time, id_lesson)
    group_data_time_lesson_pie_bar = graphics_processing.generate_group_data_time_lesson_bar(summary_group_lesson_time,
                                                                                             id_lesson)

    data_results_group_lesson = graphics_processing.generate_group_data_results_lesson(summary_group_lesson_results,
                                                                                       id_lesson)
    data_bar_results_group_lesson = graphics_processing.generate_data_results_activity_bar_grouped(
        data_results_group_lesson)
    data_pie_results_group_lesson = graphics_processing.generate_data_result_general(data_results_group_lesson)

    time_series_group_lesson_row = plotting_tool.generate_time_series_group_lesson_metrics(
        group_lesson_data_ts_processed, metrics,
        most_long_time_serie_data_ts, users_colors,
        complementary_title)
    histogram_group_lesson_row = plotting_tool.generate_row_histogram_metrics_lessons_unified(
        consolidate_metrics_group_unified,
        colors_metrics,
        metrics,
        complementary_title)
    time_group_lesson_row = plotting_tool.generate_row_time_group_lesson(group_data_time_lesson,
                                                                         group_data_time_lesson_pie_bar,
                                                                         complementary_title)

    results_group_lesson_row = plotting_tool.generate_row_results(data_results_group_lesson,
                                                                  data_pie_results_group_lesson,
                                                                  data_bar_results_group_lesson,
                                                                  complementary_title)

    rows_graphics_array = [time_series_group_lesson_row,
                           histogram_group_lesson_row,
                           time_group_lesson_row,
                           results_group_lesson_row]

    for row_graphic in rows_graphics_array:
        row_graphic.show()
        print("\n\n")
