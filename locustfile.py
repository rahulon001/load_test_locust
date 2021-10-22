from locust import HttpUser, task, between
from datetime import datetime
import sys, json
import random

constants = {}
baseurl_eat = "http://10.159.20.62:9000"
baseurl_sit = "http://10.144.108.127:9000"
baseurl_dev = "http://10.157.254.126:9001"

baseurl = baseurl_dev

get_coupon_parameters = [{"version": "v5", "start": 0, "end": 10},
                         {"version": "v5", "start": 0, "externalMerchantId": "100001000069383", "categoryId": 1,
                          "end": 10, "lat": 19.6712179806, "lng": 73.2293543592},
                         {"version": "v5", "start": 0, "categoryId": 1, "end": 10, "lat": 19.6712179806,
                          "lng": 73.2293543592}]
get_coupon_client = [{'x-client-type': 'Rjil_jiokart', "x-loginid": "9945240311"},
                     {'x-client-type': 'mops', "x-loginid": "9945240311"},
                     {'x-client-type': 'microsite', "x-loginid": "9945240311"}]
mas_id_1 = ["100001000068416","100001000068658","100001000068536","100001000068415","100001000068657","100001000068771","100001000068650","100001000068770","100001000068429"]
mas_id_2 = ["100001000068526","100001000068405","100001000068647","100001000068767","100001000068525","100001000068404","100001000068646"]

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def login_for_access_token(self):
        response = self.client.post(baseurl+"/legacy/login",
                                    data={'username': "super5", 'password': "foobar"},
                                    headers={
                                        'Content-Type': "application/x-www-form-urlencoded"
                                    },
                                    name="login_cms")
        constants["anti_forgery"] = str(response.headers['x-anti-forgery'])
        print("login_cms",constants["anti_forgery"])

    def cohort_cron(self):
        response = self.client.put(baseurl+"/coupons/v1/coupons/merchants/initiate-jpm-cohort-sync",
                                    data=json.dumps({}),
                                    name="cohort_cron")
        print("cohort_cron", response)

    def cohort_sync(self):
        response = self.client.post(baseurl+"/coupons/v1/coupons/merchants/cohort-sync",
                                    data=json.dumps({"cohorts": [{"id": datetime.now().microsecond,
                                                  "name": "Cohort" + str(datetime.now().microsecond),
                                                  "added_merchants": [random.choice(mas_id_1), random.choice(mas_id_2)],
                                                  "removed_merchants": []}]}),
                                    headers={
                                        'Content-Type': 'application/json',
                                        'X-Anti-Forgery': constants["anti_forgery"]
                                    },
                                    name="cohort_sync")
        print("cohort_sync", response.text)


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
        self.cohort_cron()

    def on_start(self):
        """
        on_start is called when a Locust start before,
        any task is scheduled
        """
        self.login_for_access_token()
