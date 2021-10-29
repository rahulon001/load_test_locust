from locust import HttpUser, task, between, constant
from datetime import datetime
import sys, json
import random

constants = {}

mas_id_1 = ["100001000068416", "100001000068658", "100001000068536", "100001000068415", "100001000068657",
            "100001000068771", "100001000068650", "100001000068770", "100001000068429"]
mas_id_2 = ["100001000068526", "100001000068405", "100001000068647", "100001000068767", "100001000068525",
            "100001000068404", "100001000068646"]
replacement_mas_id = ["100002000027555", "100001000073658"]
user_name = [("super5", "foobar"),
             ("harsh.super", "foobar")]
baseurl_eat = "http://10.159.20.62:9000"
baseurl_sit_nginx = "http://10.144.62.107:9000"
baseurl_sit = "http://10.144.108.128:9000"
baseurl_dev = "http://10.157.254.126:9001"

"""
set the environment here
"""
base_url = baseurl_sit

anti_forgery = 0

cohort_id = datetime.now().microsecond


# class WithSession(HttpUser):
#     wait_time = between(1, 5)
#
#     def on_start(self):
#         self.username, self.password = user_name.pop()
#         print("username{0} , password {1}".format(self.username, self.password))
#         response = self.client.post(base_url + "/legacy/login",
#                                     data={'username': self.username, "password": self.password},
#                                     headers={
#                                         'Content-Type': "application/x-www-form-urlencoded"
#                                     },
#                                     name="login_cms")
#         self.anti_forgery = str(response.headers['x-anti-forgery'])
#         print("login_cms", response.text)
#
#     def cohort_cron(self):
#         response = self.client.put(base_url + "/coupons/v1/coupons/merchants/initiate-jpm-cohort-sync",
#                                    data=json.dumps({}),
#                                    headers={
#                                        'X-Anti-Forgery': self.anti_forgery
#                                    },
#                                    name="cohort_cron")
#         print("cohort_cron", response.text)
#
#     def cohort_sync(self):
#         wait_time = constant(10)
#         body = {"cohorts": [{"id": cohort_id,
#                              "name": "Cohort" + str(cohort_id),
#                              "added_merchants": [random.choice(mas_id_1),
#                                                  random.choice(mas_id_2)],
#                              "removed_merchants": []}]}
#
#         response = self.client.post(base_url + "/coupons/v1/coupons/merchants/cohort-sync",
#                                     data=json.dumps(body),
#                                     headers={
#                                         'Content-Type': 'application/json',
#                                         'X-Anti-Forgery': self.anti_forgery
#                                     },
#                                     name="cohort_sync")
#         print("cohort_sync", response.text)
#
#     def cohort_update(self):
#         body = {"cohorts": [{"id": cohort_id,
#                              "name": "Cohort" + str(cohort_id),
#                              "added_merchants": [random.choice(mas_id_1),
#                                                  random.choice(mas_id_2)],
#                              "removed_merchants": [random.choice(mas_id_1)]}]}
#
#         response = self.client.post(base_url + "/coupons/v1/coupons/merchants/cohort-sync",
#                                     data=json.dumps(body),
#                                     headers={
#                                         'Content-Type': 'application/json',
#                                         'X-Anti-Forgery': self.anti_forgery
#                                     },
#                                     name="cohort_update")
#         print("cohort_sync", response.text)
#
#     @task(1)
#     def user_workflow(self):
#         sys.stdout.flush()
#         self.cohort_sync()
#         self.cohort_cron()
#         self.cohort_update()
#         self.cohort_cron()


class WithoutSession(HttpUser):
    wait_time = constant(5)

    def get_coupons_1(self):
        get_coupon_parameters = [
            {"version": "v5", "start": 0, "end": 10}
        ]
        para = random.choice(get_coupon_parameters)

        get_coupon_client = [
            {'x-client-type': 'mpos', "x-loginid": "9945240311"},
            {'x-client-type': 'microsite', "x-loginid": "9945240311"}]

        client = random.choice(get_coupon_client)

        response = self.client.get(base_url + "/coupons/v1/coupons/",
                                   params=para,
                                   headers=client,
                                   name="get_coupon_api_1")
        print("request_param_1", para)
        print("client_1", client)
        print("get_coupon_api_1", response)

    def get_coupons_2(self):
        get_coupon_parameters = [
            {"version": "v5", "externalMerchantId": random.choice(mas_id_1), "start": 0, "end": 10,
             "categoryId": 1, "lat": 19.6712179806, "lng": 73.2293543592, "validFromLimit": 26 - 10 - 2021}
        ]
        para = random.choice(get_coupon_parameters)

        get_coupon_client = [
            {'x-client-type': 'mpos', "x-loginid": "9945240311"},
            {'x-client-type': 'microsite', "x-loginid": "9945240311"}]

        client = random.choice(get_coupon_client)

        response = self.client.get(base_url + "/coupons/v1/coupons/",
                                   params=para,
                                   headers=client,
                                   name="get_coupon_api_2")
        print("request_param_2", para)
        print("client_2", client)
        print("get_coupon_api_2", response)

    def get_coupons_3(self):
        response = self.client.get(base_url + "/coupons/v1/coupons/",
                                   params={"version": "v5", "start": 0, "categoryId": 1, "end": 30, "lat": 19.0793547,
                                           "lng": 72.99920130000001
                                           },
                                   headers={'x-client-type': 'microsite', "x-loginid": "9945240311"},
                                   name="get_coupon_api_3")
        # print("request_param_3", para)
        # print("client_3", client)
        print("get_coupon_api_3", response)

    def get_coupons_4(self):
        get_coupon_parameters = [
            {"version": "v5", "start": 0, "end": 10, "query": "off"}
        ]
        para = random.choice(get_coupon_parameters)

        get_coupon_client = [
            {'x-client-type': 'mpos', "x-loginid": "9945240312"},
            {'x-client-type': 'microsite', "x-loginid": "9945240313"}]

        client = random.choice(get_coupon_client)

        response = self.client.get(base_url + "/coupons/v1/coupons/",
                                   params=para,
                                   headers=client,
                                   name="get_coupon_api_4")
        print("request_param_4", para)
        print("client_4", client)
        print("get_coupon_api_4", response)

    def b2b_replacement_api_1(self):
        response = self.client.post(
            base_url + "/coupons/v1/coupons/merchant/" + random.choice(
                mas_id_1) + "/fc/coupons?sort=earliest-expiry&sort-order=asc",
            headers={
                'Content-Type': 'application/json',
                'x-client-type': 'mpos'
            },
            data=json.dumps({"start": 0, "end": 10}),
            name="b2b_replacement_api_1")
        print("b2b_replacement_api_1", response)

    def b2b_replacement_api_2(self):
        response = self.client.post(
            base_url + "/coupons/v1/coupons/merchant/" + random.choice(
                mas_id_1) + "/fc/coupons?sort=earliest-expiry&sort-order=asc",
            headers={
                'Content-Type': 'application/json',
                'x-client-type': 'mpos'
            },
            data=json.dumps({"status": "active", "start": 0, "end": 10, "sku": 22221133}),
            name="b2b_replacement_api_2")
        print("b2b_replacement_api_2", response)

    def b2b_replacement_api_3(self):
        response = self.client.post(
            base_url + "/coupons/v1/coupons/merchant/" + random.choice(
                mas_id_1) + "/fc/coupons?sort=earliest-expiry&sort-order=asc",
            headers={
                'Content-Type': 'application/json',
                'x-client-type': 'mpos'
            },
            data=json.dumps({"start": 0, "end": 10, "sku": 22221133}),
            name="b2b_replacement_api_3")
        print("b2b_replacement_api_3", response)

    @task(5)
    def user_workflow(self):
        sys.stdout.flush()
        # self.get_coupons_1()
        # self.get_coupons_2()
        # self.get_coupons_3()
        self.get_coupons_4()
        # self.b2b_replacement_api_1()
        # self.b2b_replacement_api_2()
        # self.b2b_replacement_api_3()
