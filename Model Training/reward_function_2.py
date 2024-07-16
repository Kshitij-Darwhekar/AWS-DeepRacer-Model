# Result : 
# My Qualifying Time: 01:25.926 (Under 2 minutes but room for improvment)
# Best Time World : 00:55.530
# Best Time India : 00:56.531
# Best Time Asia Pacific: 00:56.531
# My Rank: 337/617 (India)




def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    steering_angle = params['steering_angle']
    is_crashed = params['is_crashed']
    progress = params['progress']
    # steps = params['steps']


    SPEED_THRESHOLD = 1.0  # Adjust this value based on your track's speed dynamics
    ABS_STEERING_THRESHOLD = 15.0 # Steering angle threshold
    TOTAL_NUM_STEPS = 300    # Total No of steps to complete a Lap

    # Calculate markers that are at varying distances from the center
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    

    # Base reward
    reward = 1e-3

    # Reward based on distance from the center
    if all_wheels_on_track:

        if distance_from_center <= marker_1:
            reward += 3.0
        elif distance_from_center <= marker_2:
            reward += 1.5
        elif distance_from_center <= marker_3:
            reward += 0.5
        else:
            reward = 1e-3  # likely off track or far from center

        # Speed Reward
        speed_diff = abs(1.0 - speed)
        max_speed_diff = 0.2

        if speed_diff < max_speed_diff:
            reward = 1 - (speed_diff/max_speed_diff)**0.5
        else:
            reward = 0.001

        # Ensure the reward for staying on track and a good distance from the center
        if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
            reward += 1.0
        
        # Penalize if car steer too much to prevent zigzag
        abs_steering = abs(steering_angle)
        if abs_steering > ABS_STEERING_THRESHOLD:
            reward *= 0.8

    

    #Check if the bot is crashed
    if is_crashed is True:
        reward = 1e-3
    else:
        reward += 1.0

    if not all_wheels_on_track:
        reward = 1e-3   # Severe penalty for going off the track 
    
    # Progress reward
    progress_reward = progress / 100.0  # Normalize progress to [0, 1]
    reward += progress_reward
    
    
    # Always return a float value
    return float(reward)
