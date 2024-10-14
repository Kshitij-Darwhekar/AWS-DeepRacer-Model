def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    speed = params['speed']
    is_crashed = params['is_crashed']

    SPEED_THRESHOLD = 1.0
    MAX_REWARD = 10.0  # Maximum reward for optimal performance
    MIN_REWARD = 1e-3  # Minimum reward for out-of-track or crashed scenarios
    

    # Start with a default low reward
    reward = MIN_REWARD
    
    # Calculate markers for distance from center
    markers = [0.1, 0.2, 0.3, 0.4, 0.5]
    marker_rewards = [3.0, 2.5, 1.5, 1.0, 0.5]
    
    # Reward for being closer to the center of the track
    if all_wheels_on_track:
        for i, marker in enumerate(markers):
            if distance_from_center <= marker * track_width:
                reward += marker_rewards[i]
                break  # Stop checking further if we found a marker

    # Speed reward (penalize for low speed, reward for optimal speed)
    if speed < SPEED_THRESHOLD:
        reward -= 0.5  # Penalty for going too slow
    elif speed >= SPEED_THRESHOLD:
        reward += 1.2  # Reward for maintaining optimal speed
    
    SPEED_DIFF = SPEED_THRESHOLD - speed #difference bewtween speed threshold and speed of the bot
    MAX_SPEED_DIFF = 0.2                 # Maximum allowed speed diff. (1.0 - 0.8 = 0.2)
    
    if SPEED_DIFF <= MAX_SPEED_DIFF:
        reward += 1.2                       # Reward for difference less than or equal to 0.2
    elif SPEED_DIFF > MAX_SPEED_DIFF:
        reward -= 0.5                       # Penalty for difference more than 0.2

    # Encourage staying on the track
    if all_wheels_on_track and (0.5 * track_width - distance_from_center) >= 0.05:
        reward += 1.0  # Additional reward for being well-positioned on the track

    # Check if the bot is crashed
    if is_crashed:
        return float(MIN_REWARD)  # Return minimum reward on crash

    # Normalize reward to ensure it's within acceptable bounds
    reward = max(reward, MIN_REWARD)  # Ensure we don't go below the minimum reward
    reward = min(reward, MAX_REWARD)  # Cap the maximum reward

    # Return the final reward as a float
    return float(reward)
