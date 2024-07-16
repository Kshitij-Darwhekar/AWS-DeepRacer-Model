def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    abs_steering = abs(params['steering_angle'])
    is_crashed = params['is_crashed']


    SPEED_THRESHOLD = 1.0  # Adjust this value based on your track's speed dynamics
    ABS_STEERING_THRESHOLD = 15.0 # Steering angle threshold

    # Calculate markers that are at varying distances from the center
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_3 = 0.3 * track_width
    marker_4 = 0.4 * track_width
    marker_5 = 0.5 * track_width

    # Base reward
    reward = 1e-3

    # Reward based on distance from the center
    if all_wheels_on_track:

        if distance_from_center <= marker_1 and all_wheels_on_track:
            reward += 3.0
        elif distance_from_center <= marker_2 and all_wheels_on_track:
            reward += 2.5
        elif distance_from_center <= marker_3 and all_wheels_on_track:
            reward += 1.5
        elif distance_from_center <= marker_4 and all_wheels_on_track:
            reward += 1.0 
        elif distance_from_center <= marker_5 and all_wheels_on_track:
            reward += 0.5
        else:
            reward = 1e-3  # likely off track or far from center

        # Additional reward for speed
        if speed < SPEED_THRESHOLD:
            reward -= 0.5  # Penalize for going too slow
        else:
            reward += 1.2  # Reward for going above the speed threshold

        # Ensure the reward for staying on track and a good distance from the center
        if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
            reward += 1.0
        
        # Penalize if car steer too much to prevent zigzag
        if abs_steering > ABS_STEERING_THRESHOLD:
            reward *= 0.8

    #Check if the bot is crashed
    if is_crashed is True:
        reward = 1e-3
    else:
        reward += 0.5

    # Always return a float value
    return float(reward)
