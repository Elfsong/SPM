import redis


class data_layer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6379
        self.pool_instance = redis.ConnectionPool(host=self.host, port=self.port)
        self.r = redis.Redis(connection_pool=self.pool_instance)

    def register_new_customer(self, username_dict):
        print(username_dict)
        try:
            self.r.hmset("ddd", username_dict)
            return True
        except Exception as e:
            print(e)
            return False
