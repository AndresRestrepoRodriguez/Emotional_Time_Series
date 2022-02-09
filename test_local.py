from time_series import processing_ts
import pandas as pd
import seaborn as sns
sns.set()
sns.set_style("whitegrid")
#%matplotlib inline

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

path_data = "data_1secs_extra_exe.csv"
data = pd.read_csv(path_data)

data_ts = processing_ts.process_datetime(data)
activities = processing_ts.process_activities(data_ts)
unique_act = processing_ts.get_unique_activities(activities)
diff_time_activities = processing_ts.get_time_diff_activities(activities)
print(diff_time_activities)


