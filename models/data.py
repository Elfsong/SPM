import redis


class data_layer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 6379
        self.pool_instance = redis.ConnectionPool(host=self.host, port=self.port)
        self.r = redis.Redis(connection_pool=self.pool_instance)

    def register_new_customer(self, username_dict):
        # print(username_dict)
        try:
            self.r.hmset("user:"+username_dict["username"], username_dict)
            print("Write Successful!")
            return True
        except Exception as e:
            print(e)
            return False

    def login_check(self, username, password):
        # Does the username is a manager
        try:
            userinfo = self.r.hgetall("manager:"+username)
            if userinfo and userinfo["password"] == password:
                return True, userinfo
        except Exception as e:
            print(e)
            return False, None

        # Dees the username is a user
        try:
            userinfo = self.r.hgetall("user:"+username)
            if userinfo and userinfo["password"] == password:
                return True, userinfo
        except Exception as e:
            print(e)
            return False, None
