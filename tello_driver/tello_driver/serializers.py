from rclpy.time import Time

from nav_msgs.msg import Odometry

from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import Imu
from tello_msgs.msg import FlightStats
from tellopy._internal.tello import LogData, FlightData


def generate_odom_msg(
    time: Time, odom_frame_id: str, data: LogData
) -> Odometry:
    msg = Odometry()

    msg.header.stamp = time.to_msg()
    msg.header.frame_id = odom_frame_id

    # Note that this pose is very inaccurate.
    msg.pose.pose.position.x = data.mvo.pos_x / 10
    msg.pose.pose.position.y = -data.mvo.pos_y / 10
    msg.pose.pose.position.z = data.mvo.pos_z / 10

    msg.pose.pose.orientation.x = data.imu.q1
    msg.pose.pose.orientation.y = -data.imu.q2
    msg.pose.pose.orientation.z = -data.imu.q3
    msg.pose.pose.orientation.w = data.imu.q0

    msg.twist.twist.linear.x = data.mvo.vel_x
    msg.twist.twist.linear.y = data.mvo.vel_x
    msg.twist.twist.linear.z = data.mvo.vel_x

    return msg


def generate_imu_msg(time: Time, imu_frame_id: str, data: LogData) -> Imu:
    msg = Imu()

    msg.header.frame_id = imu_frame_id
    msg.header.stamp = time.to_msg()

    msg.orientation.x = data.imu.q1
    msg.orientation.y = -data.imu.q2
    msg.orientation.z = -data.imu.q3
    msg.orientation.w = data.imu.q0

    msg.angular_velocity.x = data.imu.gyro_x
    msg.angular_velocity.y = data.imu.gyro_y
    msg.angular_velocity.z = data.imu.gyro_z

    msg.linear_acceleration.x = data.imu.acc_x
    msg.linear_acceleration.y = data.imu.acc_y
    msg.linear_acceleration.z = data.imu.acc_z

    return msg


def create_tf_between_odom_drone(
    time: Time, drone_frame_id: str, odom_frame_id: str, data: LogData
) -> TransformStamped:
    tf_odom_drone = TransformStamped()

    tf_odom_drone.header.stamp = time.to_msg()
    tf_odom_drone.header.frame_id = odom_frame_id
    tf_odom_drone._child_frame_id = drone_frame_id

    tf_odom_drone.transform.translation.x = data.mvo.pos_x / 10
    tf_odom_drone.transform.translation.y = -data.mvo.pos_y / 10
    tf_odom_drone.transform.translation.z = data.mvo.pos_z / 10

    # Sending 0 instead for the position since the one coming from drone is
    # not accurate
    # tf_odom_drone.transform.translation.x = 0.0
    # tf_odom_drone.transform.translation.y = 0.0
    # tf_odom_drone.transform.translation.z = 0.0

    tf_odom_drone.transform.rotation.x = data.imu.q1
    tf_odom_drone.transform.rotation.y = -data.imu.q2
    tf_odom_drone.transform.rotation.z = -data.imu.q3
    tf_odom_drone.transform.rotation.w = data.imu.q0

    return tf_odom_drone


def generate_flight_data_msg(data: FlightData) -> FlightStats:
    msg = FlightStats()

    # - Battery data
    msg.battery_low = data.battery_low
    msg.battery_lower = data.battery_lower
    msg.battery_percentage = data.battery_percentage
    msg.drone_battery_left = data.drone_battery_left
    # flight_data.drone_fly_time_left = data.drone_fly_time_left

    # =========================================================================

    # - States
    msg.battery_state = data.battery_state
    print(f"Bat State: {data.battery_state}")
    msg.camera_state = data.camera_state
    print(f"Cam State: {data.camera_state}")
    msg.electrical_machinery_state = data.electrical_machinery_state
    print(f"EM State: {data.electrical_machinery_state}")
    msg.down_visual_state = data.down_visual_state
    print(f"Down Visual State: {data.down_visual_state}")
    msg.gravity_state = data.gravity_state
    print(f"Grav State: {data.gravity_state}")
    msg.imu_calibration_state = data.imu_calibration_state
    print(f"IMU Cal State: {data.imu_calibration_state}")
    msg.imu_state = data.imu_state
    print(f"IMU State: {data.imu_state}")
    msg.power_state = data.power_state
    print(f"Power State: {data.power_state}")
    msg.pressure_state = data.pressure_state
    print(f"Pressure State: {data.pressure_state}")
    msg.wind_state = data.wind_state
    print(f"Wind State: {data.wind_state}")

    # =========================================================================

    # - Stats
    msg.drone_hover = data.drone_hover
    print(f"Drone Hover: {data.drone_hover}")
    msg.em_open = data.em_open
    print(f"EM Open: {data.em_open}")
    msg.em_sky = data.em_sky
    print(f"EM Sky: {data.em_sky}")
    msg.em_ground = data.em_ground
    print(f"EM Ground: {data.em_ground}")
    msg.factory_mode = data.factory_mode
    print(f"Factory Mode: {data.factory_mode}")
    msg.fly_mode = data.fly_mode
    print(f"Fly Mode: {data.fly_mode}")
    # flight_data.fly_time = data.fly_time
    print(f"Fly Time: {data.fly_time}")
    msg.front_in = data.front_in
    print(f"Front In: {data.front_in}")
    msg.front_lsc = data.front_lsc
    print(f"Front LSC: {data.front_lsc}")
    msg.front_out = data.front_out
    print(f"Front Out: {data.front_out}")

    # =========================================================================

    # - Sensors
    msg.fly_speed = data.fly_speed
    print(f"Fly Speed: {data.fly_speed}")
    msg.east_speed = data.east_speed
    print(f"East Speed: {data.east_speed}")
    msg.ground_speed = data.ground_speed
    print(f"Ground Speed: {data.ground_speed}")
    msg.height = data.height
    print(f"Height: {data.height}")
    msg.light_strength = data.light_strength
    print(f"Light Strength: {data.light_strength}")
    msg.north_speed = data.north_speed
    print(f"North Speed: {data.north_speed}")
    msg.temperature_high = data.temperature_height
    print(f"Temperature High: {data.temperature_height}")

    # =========================================================================

    # - Other
    msg.outage_recording = data.outage_recording
    msg.smart_video_exit_mode = data.smart_video_exit_mode
    # flight_data.throw_fly_timer = data.throw_fly_timer

    # =========================================================================

    # - WiFi
    msg.wifi_disturb = data.wifi_disturb
    print(f"WiFi Disturb: {data.wifi_disturb}")
    msg.wifi_strength = data.wifi_strength
    print(f"WiFi Strength: {data.wifi_strength}")

    return msg
