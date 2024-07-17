
def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    steering_angle = params['steering_angle']
    is_crashed = params['is_crashed']
    progress = params['progress']


    SPEED_THRESHOLD = 1.0  # Adjust this value based on your track's speed dynamics
    ABS_STEERING_THRESHOLD = 20.0 # Steering angle threshold

    # Base reward
    reward = 1e-3

    # Calculate markers that are at varying distances from the center
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    

    # Reward based on distance from the center

    if distance_from_center <= marker_1 and all_wheels_on_track:
        reward += 3.0
    elif distance_from_center <= marker_2 and all_wheels_on_track:
        reward += 1.5
    elif distance_from_center <= marker_3 and all_wheels_on_track:
        reward += 0.5
    else:
        reward = 1e-3  # likely off track or far from center

    # Speed Reward
    speed_diff = abs(1.0 - speed)
    max_speed_diff = 0.2

    if speed_diff < max_speed_diff:
        reward += 3.0 * (1 - (speed_diff/max_speed_diff)**2)
    else:
        reward -= 0.5 * ((speed_diff - max_speed_diff)/max_speed_diff)**2

    # Ensure the reward for staying on track and a good distance from the center
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward += 1.0
        
    # Penalize if car steer too much to prevent zigzag
    abs_steering = abs(steering_angle)
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8 + 0.2 * (ABS_STEERING_THRESHOLD/abs_steering)

    
    #Check if the bot is crashed
    if is_crashed is True:
        reward = 1e-3
    else:
        reward += 1.0
    
    # Progress reward
    progress_reward = progress / 100.0  # Normalize progress to [0, 1]
    reward += progress_reward
    
    
    # Normalize Reward Function
    reward = max(1e-3, reward)

    # Always return a float value
    return float(reward)
