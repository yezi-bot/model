include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  -- slam算法跟随的坐标系ID
  tracking_frame = "base_link",
  -- 发布map到odom之间的位姿态
  published_frame = "odom",
  odom_frame = "odom",
  -- 是否提供里程计数据
  provide_odom_frame = false,
  --只发布二维姿态
  publish_frame_projected_to_2d = true,
  use_pose_extrapolator = true,
  use_odometry = true,
  use_nav_sat = false,
  use_landmarks = false,

  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  -- 不分割
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  -- 查找变换超时秒数
  lookup_transform_timeout_sec = 0.2,
  -- 发布submap的周期间隔
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  -- 测距仪的采样率
  rangefinder_sampling_ratio = 1.,
  -- 里程计数据采样率
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

MAP_BUILDER.use_trajectory_builder_2d = true
TRAJECTORY_BUILDER_2D.min_range = 0.10
-- 限制在雷达最大扫描范围内，越小越精确
TRAJECTORY_BUILDER_2D.max_range = 3.5
--传感器数据超出有效范围最大值
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 3.
-- 不使用IMU数据
TRAJECTORY_BUILDER_2D.use_imu_data = false
-- 使用实时回环检测来进行前端的扫描匹配
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true 
--提高对运动的敏感度
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(0.1)

-- Fast csm的最低分数，高于此分数才进行优化。
POSE_GRAPH.constraint_builder.min_score = 0.65
-- 全局定位最小分数，低于此分数则认为目前全局定位不准确
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7

-- 设置0可关闭全局SLAM
-- POSE_GRAPH.optimize_every_n_nodes = 0

return options
