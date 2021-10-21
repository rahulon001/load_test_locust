from locust import HttpUser, task, between
import time
import sys
import random

constants = {}
get_coupon_parameters = [{"version": "v5", "start": 0, "end": 10}, {"version": "v5", "start": 0, "externalMerchantId": "100001000069383", "categoryId": 1, "end": 10, "lat": 19.6712179806, "lng": 73.2293543592}, {"version": "v5", "start": 0, "categoryId": 1, "end": 10, "lat": 19.6712179806, "lng": 73.2293543592}]
get_coupon_client = [{'x-client-type':'Rjil_jiokart',"x-loginid" : "9945240311"}, {'x-client-type':'mops', "x-loginid" : "9945240311"}, {'x-client-type':'microsite', "x-loginid" : "9945240311"}]


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def get_coupons(self):
        response = self.client.get("http://10.144.108.127:9000/coupons/v1/coupons/",
                                   params=random.choice(get_coupon_parameters),
                                   headers=random.choice(get_coupon_client),
                                   name="get_coupons")
        print(response)

    @task(1)
    def user_workflow(self):
        sys.stdout.flush()
        self.get_coupons()

#
# class WebsiteUser(HttpUser):
#     min_wait = 1000
#     max_wait = 1000
#     tasks = [QuickstartUser]
#     host = "https:localhost:8089"
