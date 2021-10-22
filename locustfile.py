from locust import HttpUser, task, between
from datetime import datetime
import sys, json
import random

constants = {}
baseurl_eat = "http://10.159.20.62:9000"
baseurl_sit = "http://10.144.108.127:9000"

get_coupon_parameters = [{"version": "v5", "start": 0, "end": 10},
                         {"version": "v5", "start": 0, "externalMerchantId": "100001000069383", "categoryId": 1,
                          "end": 10, "lat": 19.6712179806, "lng": 73.2293543592},
                         {"version": "v5", "start": 0, "categoryId": 1, "end": 10, "lat": 19.6712179806,
                          "lng": 73.2293543592}]
get_coupon_client = [{'x-client-type': 'Rjil_jiokart', "x-loginid": "9945240311"},
                     {'x-client-type': 'mops', "x-loginid": "9945240311"},
                     {'x-client-type': 'microsite', "x-loginid": "9945240311"}]
mas_id_1 = ["100001000071385", "100001000069193", "100001000183843"]

body1 = {"cohorts": [{"id": datetime.now().microsecond,
                                                  "name": "Cohort" + str(datetime.now().microsecond),
                                                  "added_merchants": [random.choice(mas_id_1)],
                                                  "removed_merchants": []}]}
body = json.dumps(body1)


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def login_for_access_token(self):
        response = self.client.post(baseurl_sit+"/legacy/login",
                                    data={'username': "super5", 'password': "foobar"},
                                    headers={
                                        'Content-Type': "application/x-www-form-urlencoded"
                                    },
                                    name="login_for_x_anti-forgery")
        constants["anti_forgery"] = str(response.headers['x-anti-forgery'])
        print(constants["anti_forgery"])

    def cohort_sync(self):
        response = self.client.post(baseurl_sit+"/coupons/v1/coupons/merchants/cohort-sync",
                                    data=body,
                                    headers={
                                        'Content-Type': 'application/json',
                                        'X-Anti-Forgery': constants["anti_forgery"]
                                    },
                                    name="cohort_sync")
        print(response.text)

    # def get_coupons(self):
    #     response = self.client.get("http://10.144.108.127:9000/coupons/v1/coupons/",
    #                                params=random.choice(get_coupon_parameters),
    #                                headers=random.choice(get_coupon_client),
    #                                name="get_coupons")
    #     print(response)

    @task(1)
    def user_workflow(self):
        sys.stdout.flush()
        self.cohort_sync()

    def on_start(self):
        """
        on_start is called when a Locust start before,
        any task is scheduled
        """
        self.login_for_access_token()
