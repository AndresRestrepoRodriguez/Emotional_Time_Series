num_users = 19
lesson_number = 1
lessons = c("1", "2", "3", "4")
users_id = seq(1, num_users, by=1)
users_id_str = sprintf("%d",users_id)
path_data = '/path/data/EDaLI/id_%d/lesson_%s/emotional_data.csv'
metrics = c("engagement", "interest", "stress", "relax", "focus", "excitation")

list_lessons = list()
for (lesson in lessons){
  list_users = list()
  for (user in users_id){
    new_path = sprintf(path_data, user, lesson)
    df_data = read.csv(new_path)
    data_user = as.list(df_data)
    list_users = append(list_users, list(data_user))
  }
  names(list_users) = c(sprintf("%d",users_id))
  list_lessons = append(list_lessons, list(list_users))
}
names(list_lessons) = lessons


list_lessons_metrics = list()
for (lesson in lessons){
  list_metrics = list()
  for (metric in metrics){
    tmp_list = list()
    for (user in users_id_str){
      data_tmp = list_lessons[[lesson]][[user]][metric]
      tmp_list = append(tmp_list, data_tmp)
    }
    names(tmp_list) = c(users_id_str)
    list_metrics = append(list_metrics, list(tmp_list))
  }
  names(list_metrics) = c(metrics)
  list_lessons_metrics = append(list_lessons_metrics, list(list_metrics))
}
names(list_lessons_metrics) = lessons

#data_cluster = list_lessons_metrics[['1']][['engagement']]
library("dtwclust")


# Define overall configuration
cfgs_pam <- compare_clusterings_configs(
  types = c("p"),
  k = 2L:18L,
  controls = list(
    partitional = partitional_control(
      iter.max = 50L,
      nrep = 1L
    )
  ),
  preprocs = pdc_configs(
    type = "preproc",
    # shared
    none = list(),
    zscore = list(center = c(FALSE)),
    share.config = c("p")
  ),
  distances = pdc_configs(
    type = "distance",
    sbd = list(),
    dtw = list(),
    gak = list(),
    sdtw = list(),
    share.config = c("p")
  ),
  centroids = pdc_configs(
    type = "centroid",
    partitional = list(
      pam = list()
    )
  )
)


# Define overall configuration
cfgs_shape <- compare_clusterings_configs(
  types = c("p"),
  k = 2L:18L,
  controls = list(
    partitional = partitional_control(
      iter.max = 50L,
      nrep = 1L
    )
  ),
  preprocs = pdc_configs(
    type = "preproc",
    # shared
    zscore = list(center = c(FALSE)),
    share.config = c("p")
  ),
  distances = pdc_configs(
    type = "distance",
    sbd = list(),
    dtw = list(),
    gak = list(),
    sdtw = list(),
    share.config = c("p")
  ),
  centroids = pdc_configs(
    type = "centroid",
    partitional = list(
      shape = list()
    )
  )
)

# Number of configurations is returned as attribute
num_configs_pam <- sapply(cfgs_pam, attr, which = "num.configs")
num_configs_shape <- sapply(cfgs_shape, attr, which = "num.configs")
cat("\nTotal number of configurations without considering optimizations:",
    sum(num_configs_pam) + sum(num_configs_shape),
    "\n\n")


vi_evaluators <- cvi_evaluators("internal", ground.truth=NULL)
score_fun <- vi_evaluators$score
pick_fun <- vi_evaluators$pick


# proceso iterativo
# Partitional
methods = c("pam", "shape")
list_lessons_metrics_results_pam_shape_1 = list()
for (lesson in lessons){
  list_metrics_results = list()
  for (metric in metrics){
    list_metric_tmp = list()
    data_cluster = list_lessons_metrics[[lesson]][[metric]]
    
    comparison_short <- compare_clusterings(data_cluster, types = c("p"), configs = cfgs_pam_1,
                                            trace = TRUE, score.clus = score_fun, pick.clus = pick_fun,
                                            return.objects = TRUE)
    
    comparison_short2 <- compare_clusterings(data_cluster, types = c("p"), configs = cfgs_shape_1,
                                             trace = TRUE, score.clus = score_fun, pick.clus = pick_fun,
                                             return.objects = TRUE)
    list_metric_tmp = append(list_metric_tmp, list(comparison_short$pick))
    list_metric_tmp = append(list_metric_tmp, list(comparison_short2$pick))
    names(list_metric_tmp) = methods
    list_metrics_results = append(list_metrics_results, list(list_metric_tmp))
  }
  names(list_metrics_results) = metrics
  list_lessons_metrics_results_pam_shape_1 = append(list_lessons_metrics_results_pam_shape_1, list(list_metrics_results))
}
names(list_lessons_metrics_results_pam_shape_1) = lessons