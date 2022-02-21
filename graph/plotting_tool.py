import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime

sns.set()
sns.set_style("whitegrid")


def get_plot_ts(dataframe_ts, metrics_list, colors_metrics, zone_data, dict_colors, unique_actitivities):
    fig, ax = plt.subplots(figsize=(12, 7))
    for i in metrics_list:
        ax.plot(dataframe_ts.index.values,
                dataframe_ts[i],
                label=i,
                color=colors_metrics.get(i))
    ax.set_title('Record Performance Metrics Participant Id. ' + str(
        int(re.findall(r'\d+', dataframe_ts['user_id'].iloc[0])[0]) + 1) + ' \nInteraction with lesson No. ' +
                 dataframe_ts['lesson'].iloc[0] + ' - language: Portuguese\n', fontsize=16, fontweight='bold')
    ax.set_xlabel('Time', fontsize=14, fontweight='bold')
    ax.set_ylabel('Performance Metrics Values', fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%M:%S"))
    lines = ax.get_lines()
    zones = list()
    for i in zone_data:
        zones.append(ax.axvspan(i[1], i[2], facecolor=dict_colors.get(i[0]), alpha=0.45))
        legend1 = plt.legend([line for line in lines], metrics_list, bbox_to_anchor=(1, 1), loc='upper left',
                             prop={'size': 13})
    legend1.set_title("Metrics", prop={'size': 13, 'weight': 'bold'})
    by_label = dict(zip(unique_actitivities, zones))
    legend2 = plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1, 0.25), loc='lower left',
                         prop={'size': 13})
    legend2.set_title("Activities", prop={'size': 13, 'weight': 'bold'})
    ax.add_artist(legend1)
    ax.add_artist(legend2)
    plt.gca().add_artist(legend1)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.show()


def generate_time_series_plot(activities_info, dataframe_ts, metrics, colors_metrics, colors_activities,
                              complementary_title):
    fig = go.Figure()
    for metric in metrics:
        fig.add_trace(go.Scatter(x=dataframe_ts.index, y=dataframe_ts[metric], line={'color': colors_metrics[metric]},
                                 name=metric))
    for activity in activities_info:
        fig.add_vrect(
            x0=activity[1], x1=activity[2],
            fillcolor=colors_activities[activity[0]], opacity=0.5,
            layer="below", line_width=0, annotation_text='<b>' + activity[0] + '</b>', annotation_position="top left"
        )
    fig.update_annotations(font_size=15, font_color='#000000')
    fig.update_layout(
        title={'text': f' <b> Record Performance Metrics <br> '
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        xaxis_title="Time",
        yaxis_title="Performance Metrics Value",
        legend_title="Metrics")
    fig.update_xaxes(
        tickformat="%H:%M:%S",
        tickangle=-45,
        range=[dataframe_ts.index[0] - datetime.timedelta(seconds=5),
               dataframe_ts.index[-1] + datetime.timedelta(seconds=5)])
    return fig


def generate_hist_by_metric(dataframe_ts, metric, colors_metrics):
    values = dataframe_ts[metric].values
    return go.Histogram(x=values, meta={'colorbar': colors_metrics[metric], 'title': 'Hola mundo'}, name=metric)


def gen_table(data_time_activity, header_table):
    transform_data = np.array(data_time_activity.copy()).T
    header_table = header_table
    table = go.Table(header=dict(values=header_table),
                     cells=dict(values=transform_data))
    return table


def generate_bar_activity_time(data_time_activity, legend_show=True):
    return go.Bar(x=data_time_activity['x_values'], y=data_time_activity['y_values'], showlegend=legend_show)


def generate_pie_activity_time(data_time_activity, legend_show=True):
    return go.Pie(values=data_time_activity["y_values"], labels=data_time_activity["x_values"], showlegend=legend_show)


def generate_bar_grouped_activity_results(data_results_activities, legend_show=True):
    data_traces = []
    count = 0
    colors = ['#EF553B', '#00CC96', '#636EFA', '#FFA15A']
    for value_name in data_results_activities['name_values']:
        trace = go.Bar(x=data_results_activities['x_values'],
                       y=data_results_activities['y_values'][count], marker_color=colors[count],
                       showlegend=legend_show)
        data_traces.append(trace)
        count += 1
    return data_traces


def generate_pie_activity_result(data_result_activity, legend_show=True):
    colors = ['#EF553B', '#00CC96', '#636EFA', '#FFA15A']
    return go.Pie(values=data_result_activity["y_values"], labels=data_result_activity["x_values"],
                  showlegend=legend_show, marker=dict(colors=colors))


def generate_heatmap_time_series(x_values, y_values):
    return go.Histogram2d(
        x=x_values,
        y=y_values,
        coloraxis="coloraxis",
        nbinsx=20, nbinsy=20
    )


def generate_row_histogram_metrics(dataframe_ts, colors_metrics, metrics, complementary_title):
    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Distribution for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Metric value',
                        y_title='Frecuency', subplot_titles=subplot_titles)
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            fig.add_trace(generate_hist_by_metric(dataframe_ts, metrics[pos_metric], colors_metrics), row, col)
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Distribution of Performance Metrics <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Metrics",
        xaxis=dict(
            title="Values"
        )
    )
    return fig


def generate_row_time(data_time_activity, data_time_bar_pie, complementary_title):
    # data_time_activity = generate_data_time_activity(json_data)
    # data_time_bar_pie = generate_data_time_activity_bar(data_time_activity)
    rows = 1
    columns = 3
    subplot_titles = ("Time by Activity", "Time by Activity Bar plot", "Time Porcentage by Activity")
    header_table = ["Activity", "Time"]
    specs = [[{'type': 'domain'}, {'type': 'bar'}, {'type': 'pie'}]]
    fig = make_subplots(rows=rows, cols=columns, specs=specs,
                        subplot_titles=subplot_titles)

    fig.add_trace(gen_table(data_time_activity, header_table), 1, 1)

    fig.add_trace(generate_bar_activity_time(data_time_bar_pie, False), 1, 2)

    fig.add_trace(generate_pie_activity_time(data_time_bar_pie), 1, 3)

    fig = go.Figure(fig)
    fig['layout']['xaxis']['title'] = 'Activity'
    fig['layout']['yaxis']['title'] = 'Time (s)'
    fig.update_layout(
        title={'text': f' <b> Time Measurement <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Activities",
    )
    return fig


def generate_row_results(data_time_activity, data_time_bar_pie, data_result_bar, complementary_title):
    # data_time_activity = generate_data_result_activity(json_data)
    # data_time_bar_pie = generate_data_result_general(data_time_activity)
    # data_result_bar = generate_data_results_activity_bar_grouped(data_time_activity)
    rows = 1
    columns = 3
    subplot_titles = ("Results by Activity", "Results by Activity Bar plot", "General Results Porcentage by Activity")
    header_table = ["Activity", "Total Questions", "Correct", "Incorrect", "Errors / Attempts"]
    specs = [[{'type': 'domain'}, {'type': 'bar'}, {'type': 'pie'}]]
    fig = make_subplots(rows=rows, cols=columns, specs=specs,
                        subplot_titles=subplot_titles)

    colors = ['red', 'green', 'blue', 'yellow']

    fig.add_trace(gen_table(data_time_activity, header_table), 1, 1)

    # fig.add_trace(generate_pie_activity_result(data_time_bar_pie), 1, 2)
    for bar_plot in generate_bar_grouped_activity_results(data_result_bar, False):
        fig.append_trace(bar_plot, 1, 2)

    fig.add_trace(generate_pie_activity_result(data_time_bar_pie), 1, 3)
    fig['layout']['xaxis']['title'] = 'Activity'
    fig['layout']['yaxis']['title'] = 'Answers'
    layout = go.Layout(barmode='group', )
    fig = go.Figure(fig, layout=layout)
    fig.update_layout(
        title={'text': f' <b> Questions Results <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
    )
    return fig


def generate_heatmap_row(dataframe_ts, metrics, complementary_title):
    subtitles_array = []
    rows = 1
    columns = len(metrics) // 2
    for metric in metrics:
        subtitles_array.append(f"Heatmap for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Time (s)',
                        y_title='Performance Metric Value', subplot_titles=subplot_titles)
    x_value_time = dataframe_ts.index
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric = metrics[pos_metric]
            y_value_metric = dataframe_ts[metric].values
            fig.add_trace(generate_heatmap_time_series(x_value_time, y_value_metric), row, col)
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Heatmap Performance Metrics <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        coloraxis={'colorscale': [(0, "white"), (0.5, "red"), (1, "blue")]}
    )
    return fig


def generate_time_series_participant_metric(dataframes_ts_lessons, metric, colors_lessons, showlegend):
    traces = []
    for key_lesson in dataframes_ts_lessons:
        data_ts = dataframes_ts_lessons[key_lesson]
        traces.append(go.Scatter(x=data_ts.index, y=data_ts[metric], name=key_lesson, legendgroup=key_lesson,
                                 line={'color': colors_lessons[key_lesson]}, showlegend=showlegend))
    return traces


def generate_time_series_partipant_metrics(dataframes_ts_lessons, metrics, df_time_series_long_xaxis, colors_lessons,
                                           complementary_title):
    # df_time_series_long_xaxis = dataframes_ts_lessons[get_most_long_time_series(df_consolidate)]

    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Time serie {metric}")
    subplot_titles = tuple(subtitles_array)

    count_metric = 0
    dict_traces_metrics = {}
    for metric in metrics:
        showlegend_value = True if count_metric == 0 else False
        dict_traces_metrics[metric] = generate_time_series_participant_metric(dataframes_ts_lessons,
                                                                              metric, colors_lessons,
                                                                              showlegend_value)
        count_metric += 1

    rows = 3
    columns = 2
    fig = make_subplots(rows=rows, cols=columns,
                        subplot_titles=subplot_titles)

    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (column - 1)
            metrics_val = metrics[pos_metric]
            traces = dict_traces_metrics[metrics_val]
            for trace in traces:
                fig.append_trace(trace, row, column)

    fig.update_layout(
        title={'text': f' <b> Performance Metric Recording Pool <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Lessons"
    )
    fig.update_xaxes(
        tickformat="%H:%M:%S",
        range=[df_time_series_long_xaxis.index[0] - datetime.timedelta(seconds=5),
               df_time_series_long_xaxis.index[-1] + datetime.timedelta(seconds=5)])

    return fig


def generate_bar_grouped_lessons_results(data_results_lessons, legend_show=True):
    data_traces = []
    count = 0
    colors = ['#EF553B', '#00CC96', '#636EFA', '#FFA15A']
    for value_name in data_results_lessons['name_values']:
        trace = go.Bar(x=data_results_lessons['x_values'],
                       y=data_results_lessons['y_values'][count], marker_color=colors[count],
                       showlegend=legend_show)
        data_traces.append(trace)
        count += 1
    return data_traces


def generate_pie_lesson_results(data_result_lessons, legend_show=True):
    colors = ['#EF553B', '#00CC96', '#636EFA', '#FFA15A']
    return go.Pie(values=data_result_lessons["y_values"], labels=data_result_lessons["x_values"],
                  showlegend=legend_show, marker=dict(colors=colors))


def generate_row_results_participant_lessons(data_time_activity, data_time_bar_pie, data_result_bar):
    # data_time_activity = generate_data_result_activity(json_data)
    # data_time_bar_pie = generate_data_result_general(data_time_activity)
    # data_result_bar = generate_data_results_activity_bar_grouped(data_time_activity)
    rows = 1
    columns = 3
    subplot_titles = ("Results by Lesson", "Results by Lesson Bar plot", "General Results Porcentage Lessons")
    header_table = ["Activity", "Total Questions", "Correct", "Incorrect", "Errors / Attempts"]
    specs = [[{'type': 'domain'}, {'type': 'bar'}, {'type': 'pie'}]]
    fig = make_subplots(rows=rows, cols=columns, specs=specs,
                        subplot_titles=subplot_titles)

    colors = ['red', 'green', 'blue', 'yellow']

    fig.add_trace(gen_table(data_time_activity, header_table), 1, 1)

    # fig.add_trace(generate_pie_activity_result(data_time_bar_pie), 1, 2)
    for bar_plot in generate_bar_grouped_lessons_results(data_result_bar, False):
        fig.append_trace(bar_plot, 1, 2)

    fig.add_trace(generate_pie_lesson_results(data_time_bar_pie), 1, 3)
    fig['layout']['xaxis']['title'] = 'Activity'
    fig['layout']['yaxis']['title'] = 'Answers'
    layout = go.Layout(barmode='group', )
    fig = go.Figure(fig, layout=layout)
    fig.update_layout(
        title={'text': ' <b> Results <br> <b>',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
    )
    return fig


def generate_bar_lessons_time(data_time_activity, legend_show=True):
    return go.Bar(x=data_time_activity['x_values'], y=data_time_activity['y_values'], showlegend=legend_show)


def generate_pie_lessons_time(data_time_activity, legend_show=True):
    return go.Pie(values=data_time_activity["y_values"], labels=data_time_activity["x_values"], showlegend=legend_show)


def generate_row_time_participant_lessons(data_time_lessons, data_time_bar_pie, complementary_title):
    # data_time_activity = generate_data_time_activity(json_data)
    # data_time_bar_pie = generate_data_time_activity_bar(data_time_activity)
    rows = 1
    columns = 3
    subplot_titles = ("Time by Lesson", "Time by Lesson Bar plot", "Time Porcentage by Lesson")
    header_table = ["Lesson", "Time"]
    specs = [[{'type': 'domain'}, {'type': 'bar'}, {'type': 'pie'}]]
    fig = make_subplots(rows=rows, cols=columns, specs=specs,
                        subplot_titles=subplot_titles)

    fig.add_trace(gen_table(data_time_lessons, header_table), 1, 1)

    fig.add_trace(generate_bar_lessons_time(data_time_bar_pie, False), 1, 2)

    fig.add_trace(generate_pie_lessons_time(data_time_bar_pie), 1, 3)

    fig = go.Figure(fig)
    fig['layout']['xaxis']['title'] = 'Lesson'
    fig['layout']['yaxis']['title'] = 'Time (s)'
    fig.update_layout(
        title={'text': f' <b> Time Measurement <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Activities",
    )
    return fig


def generate_hist_by_metric_unified(values, metric, colors_metrics):
    return go.Histogram(x=values, marker_color=colors_metrics[metric], name=metric)


def generate_row_histogram_metrics_lessons_unified(consolidate_metrics_lessons_unified, colors_metrics, metrics,
                                                   complementary_title):
    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Distribution for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Metric value',
                        y_title='Frecuency', subplot_titles=subplot_titles)
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric_value = metrics[pos_metric]
            data_values = consolidate_metrics_lessons_unified[metric_value]
            fig.add_trace(generate_hist_by_metric_unified(data_values, metric_value, colors_metrics), row, col)
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Performance Metrics Distribution Unification <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Metrics",
        xaxis=dict(
            title="Values"
        )
    )
    return fig


def generate_hist_by_metric_lessons(dataframe_ts, metric, colors_lessons, lesson, showlegend=True):
    values = dataframe_ts[metric].values
    return go.Histogram(x=values, marker_color=colors_lessons[lesson],
                        name=lesson, legendgroup=lesson, showlegend=showlegend)


def generate_row_histogram_metrics_lessons_overlay(df_consolidate_time_series, colors_lessons, metrics,
                                                   complementary_title):
    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Distribution for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Metric value',
                        y_title='Frecuency', subplot_titles=subplot_titles)
    count_legend = 0
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric_value = metrics[pos_metric]

            for lesson in df_consolidate_time_series:
                state_show_legend = True if count_legend == 0 else False
                fig.append_trace(generate_hist_by_metric_lessons(df_consolidate_time_series[lesson],
                                                                 metric_value, colors_lessons,
                                                                 lesson,
                                                                 state_show_legend), row, col)
            count_legend += 1
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Performance Metrics Distribution Overlay <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Metrics",
        xaxis=dict(
            title="Values"
        )
    )
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    return fig


def generate_heatmap_row_lessons_overlay(df_consolidate_time_series, metrics, complementary_title):
    subtitles_array = []
    rows = 1
    columns = len(metrics) // 2
    for metric in metrics:
        subtitles_array.append(f"Heatmap for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Time (s)',
                        y_title='Performance Metric Value', subplot_titles=subplot_titles)

    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric = metrics[pos_metric]
            for lesson in df_consolidate_time_series:
                x_value_time = df_consolidate_time_series[lesson].index
                y_value_metric = df_consolidate_time_series[lesson][metric].values
                fig.append_trace(generate_heatmap_time_series(x_value_time, y_value_metric), row, col)
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Heatmap Performance Metrics Overlay <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        coloraxis={'colorscale': [(0, "white"), (0.5, "red"), (1, "blue")]}
    )
    return fig


def generate_time_series_participant_metric_activity(dataframes_ts_lessons, metric, colors_lessons, showlegend):
    traces = []
    real_state_showlegend = showlegend
    for key_lesson in dataframes_ts_lessons:
        showlegend_value = real_state_showlegend
        data_activities_df = dataframes_ts_lessons[key_lesson]
        count_activity = 0
        for data_activity_df in data_activities_df:
            if showlegend_value:
                showlegend_value = True if count_activity == 0 else False
            data_ts = data_activity_df
            traces.append(go.Scatter(x=data_ts.index, y=data_ts[metric], name=key_lesson, legendgroup=key_lesson,
                                     line={'color': colors_lessons[key_lesson]}, mode="lines", showlegend=showlegend_value))
            count_activity += 1
    return traces


def generate_time_series_partipant_lesson_activity_metrics(dataframes_ts_lessons, metrics, colors_lessons,
                                                           complementary_title):
    # df_time_series_long_xaxis = dataframes_ts_lessons[get_most_long_time_series(df_consolidate)]

    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Time serie {metric}")
    subplot_titles = tuple(subtitles_array)

    count_metric = 0
    dict_traces_metrics = {}
    for metric in metrics:
        showlegend_value = True if count_metric == 0 else False
        dict_traces_metrics[metric] = generate_time_series_participant_metric_activity(dataframes_ts_lessons,
                                                                                       metric, colors_lessons,
                                                                                       showlegend_value)
        count_metric += 1

    rows = 3
    columns = 2
    fig = make_subplots(rows=rows, cols=columns,
                        subplot_titles=subplot_titles)

    for row in range(1, rows + 1):
        for column in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (column - 1)
            metrics_val = metrics[pos_metric]
            traces = dict_traces_metrics[metrics_val]
            for trace in traces:
                fig.append_trace(trace, row, column)

    fig.update_layout(
        title={'text': f' <b> Performance Metric Recording Pool <br> '
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Lessons"
    )
    return fig


def generate_row_histogram_metrics_lessons_activity_unified(consolidate_metrics_lessons_unified, colors_metrics,
                                                            metrics, complementary_title):
    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Distribution for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Metric value',
                        y_title='Frecuency', subplot_titles=subplot_titles)
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric_value = metrics[pos_metric]
            data_values = consolidate_metrics_lessons_unified[metric_value]
            fig.add_trace(generate_hist_by_metric_unified(data_values, metric_value, colors_metrics), row, col)
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Performance Metrics Distribution Unification <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Metrics",
        xaxis=dict(
            title="Values"
        )
    )
    return fig


def generate_hist_by_metric_lessons_activity(dataframe_ts, metric, colors_lessons, lesson, showlegend=True):
    values_tmp = []
    hist_activities_lesson = []
    count_activity = 0
    for activity_value in dataframe_ts:
        if showlegend:
            showlegend = True if count_activity == 0 else False
        values = activity_value[metric].values
        hist_activities_lesson.append(go.Histogram(x=values, marker_color=colors_lessons[lesson],
                                                   name=lesson, legendgroup=lesson, showlegend=showlegend))
        count_activity += 1
    return hist_activities_lesson


def generate_row_histogram_metrics_lessons_activity_overlay(df_consolidate_time_series, colors_lessons, metrics,
                                                            complementary_title):
    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Distribution for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Metric value',
                        y_title='Frecuency', subplot_titles=subplot_titles)
    count_legend = 0
    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric_value = metrics[pos_metric]

            for lesson in df_consolidate_time_series:
                state_show_legend = True if count_legend == 0 else False
                list_hist_lesson_activity = generate_hist_by_metric_lessons_activity(df_consolidate_time_series[lesson],
                                                                                     metric_value, colors_lessons,
                                                                                     lesson,
                                                                                     state_show_legend)
                for hist_activity_dist in list_hist_lesson_activity:
                    fig.append_trace(hist_activity_dist, row, col)
            count_legend += 1
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Performance Metrics Distribution Overlay <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Metrics",
        xaxis=dict(
            title="Values"
        )
    )
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    return fig


def generate_heatmap_row_lesson_activity_overlay(df_consolidate_time_series, metrics, complementary_title):
    subtitles_array = []
    for metric in metrics:
        subtitles_array.append(f"Heatmap for {metric}")
    subplot_titles = tuple(subtitles_array)
    rows = 2
    columns = len(metrics) // 2
    fig = make_subplots(rows=rows, cols=columns, x_title='Time (s)',
                        y_title='Performance Metric Value', subplot_titles=subplot_titles)

    for row in range(1, rows + 1):
        for col in range(1, columns + 1):
            pos_metric = ((row - 1) * columns) + (col - 1)
            metric = metrics[pos_metric]
            for lesson in df_consolidate_time_series:
                activities_consolidate = df_consolidate_time_series[lesson]
                for activity in activities_consolidate:
                    x_value_time = activity.index
                    y_value_metric = activity[metric].values
                    fig.append_trace(generate_heatmap_time_series(x_value_time, y_value_metric), row, col)
    fig = go.Figure(fig)
    fig.update_layout(
        title={'text': f' <b> Heatmap Performance Metrics Overlay <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        coloraxis={'colorscale': [(0, "white"), (0.5, "red"), (1, "blue")]}
    )
    return fig


def generate_row_time_participant_lessons_activity(data_time_lessons, data_time_bar_pie, complementary_title):
    # data_time_activity = generate_data_time_activity(json_data)
    # data_time_bar_pie = generate_data_time_activity_bar(data_time_activity)
    rows = 1
    columns = 3
    subplot_titles = ("Time by Lesson", "Time by Lesson Bar plot", "Time Porcentage by Lesson")
    header_table = ["Lesson", "Time"]
    specs = [[{'type': 'domain'}, {'type': 'bar'}, {'type': 'pie'}]]
    fig = make_subplots(rows=rows, cols=columns, specs=specs,
                        subplot_titles=subplot_titles)

    fig.add_trace(gen_table(data_time_lessons, header_table), 1, 1)

    fig.add_trace(generate_bar_lessons_time(data_time_bar_pie, False), 1, 2)

    fig.add_trace(generate_pie_lessons_time(data_time_bar_pie), 1, 3)

    fig = go.Figure(fig)
    fig['layout']['xaxis']['title'] = 'Lesson'
    fig['layout']['yaxis']['title'] = 'Time (s)'
    fig.update_layout(
        title={'text': f' <b> Time Measurement <br>'
                       f'{complementary_title}',
               'font': {
                   'family': "Arial",
                   'size': 18,
                   'color': '#000000'
               }},
        title_x=0.5,
        legend_title="Activities",
    )
    return fig
