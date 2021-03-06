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

    def add_new_order(self, order_info):
        try:
            current_order_number = self.r.get("order_number")
            self.r.incr("order_number")

            order_info["order_number"] = "order:" + current_order_number
            order_info["status"] = "To be Approved"
            order_info["p_date"] = "None"
            order_info["cost"] = "$" + str(int(order_info["number_box"]) * 35)
            order_info["h_number"] = "None"
            order_info["os_message"] = "None"

            self.r.hmset("order:" + current_order_number, order_info)
            return True
        except Exception as e:
            print(e)
            return False

    def find_all_order_by_username(self, username):
        order_list = self.r.keys("order:*")
        result_list = []
        for order in order_list:
            order_info = self.r.hgetall(order)
            if order_info["username"] == username:
                result_list += [order_info]
        return result_list

    def find_all_order(self):
        order_list = self.r.keys("order:*")
        result_list = []
        for order in order_list:
            order_info = self.r.hgetall(order)
            result_list += [order_info]
        return result_list

    def find_order(self, order_number):
        order_info = self.r.hgetall(order_number)
        return order_info

    def update_order_by_order_number(self, order_info):
        try:
            self.r.hmset(order_info["order_number"], order_info)
            return True
        except Exception as e:
            print(e)
            return False

    def get_email_by_order_number(self, order_number):
        try:
            username = self.r.hget(order_number, "username")
            print(username)
            email_address = self.r.hget("user:" + username, "email_address")
            return email_address
        except Exception as e:
            print(e)
            return False

