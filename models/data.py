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

    def login_check(self, username, password, title):
        try:
            userinfo = self.r.hgetall(title + ":" + username)

            if userinfo and userinfo["password"] == password:
                return True, userinfo
            else:
                return False, None

        except Exception as e:
            print(e)
            return False, ""
