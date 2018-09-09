import redis

pool_instance = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool_instance)

def register_new_customer(username_dict):
    print("KKK!")
