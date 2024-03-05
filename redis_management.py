import redis
from datetime import datetime, timedelta

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

threshold = timedelta(minutes=1)


def update_redis_data(user_identity:str):
    # take the user info into redis
    if r.exists(user_identity)==0:
        user_digit = int(user_identity[5:])
        group = 10 if int(user_digit / 100) == 0 else int(user_digit / 100)
        r.hset(user_identity, mapping={
            "visit": 0,
            "last_visit_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "rate_limit_left": 3,
            "group": group
            }
        )

    else:
        last_visit_time_str = r.hget(user_identity, 'last_visit_time')
        last_visit_time = datetime.strptime(last_visit_time_str, '%Y-%m-%d %H:%M:%S')

        # Get the current time
        current_time = datetime.now()

        # Calculate the time difference
        time_difference = current_time - last_visit_time

        # Set new rate_limit
        if time_difference < threshold: # The user visited within the last min
            new_rate_limit = 3 if int(r.hget(user_identity, 'rate_limit_left')) == 0 else int(r.hget(user_identity, 'rate_limit_left'))-1
        else: # It's been more than a min since the user's last visit.
            new_rate_limit = 3
        r.hset(user_identity, 'rate_limit_left', new_rate_limit)
        r.hincrby(user_identity, 'visit', 1)
        r.hset(user_identity, 'last_visit_time', current_time.strftime('%Y-%m-%d %H:%M:%S'))
