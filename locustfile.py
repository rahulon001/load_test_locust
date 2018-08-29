from locust import HttpLocust, TaskSet, task
import json
import sys
import random
constants={}

constants['credentials'] = {'9945240311': "jiomoney@2", '8880613625': "jiomoney@2", '9944031431': "jiomoney@2", '7204660988': "Qktest@1", '9945240316': "jiomoney@2"}

class UserBehavior(TaskSet):
    def login_for_access_token(l):
        response = l.client.post("/jm/auth/oauth/v2/token",
                                 data = {'username' :"9945240311", 'password' : "jiomoney@2", 'grant_type':"password"},
                                 headers={
                                     'Authorization': "Basic bDd4eDNlODg3NDAzYjVlZDQwZTc4Y2E4ZWRlZjY1Yzg3NTg3OmM2NDU1NjhhOTI3NzQ1YTY5NmUwZTUyZTU4NzFiZTgz",
                                     'Content-Type': "application/x-www-form-urlencoded"
                                 },
                                 name="login_for_access_token")
        constants["access_token"] = json.loads(response.text)["access_token"]
        print(response)

    def get_category(l):
        response = l.client.get("/cr/v2/coupons/category",
                                params={"client":"myjio","version":"v5"},
                                headers={'Authorization': "Bearer {}".format(constants["access_token"]),
                                         'X-API-Key': "l7xx3e887403b5ed40e78ca8edef65c87587",
                                         },
                                name="get_category")
        print(response)

    def get_favourites(l):
        response = l.client.get("/cr/v2/coupons/favorites",
                                params={"version":"v5"},
                                headers={
                                    'Authorization': "Bearer {}".format(constants["access_token"]),
                                    'X-API-Key': "l7xx3e887403b5ed40e78ca8edef65c87587",
                                },
                                name="get_favourites")
        print(response)

    def get_coupons(l):
        response = l.client.get("/cr/v2/coupons",
                                params={"categoryId":"1","start":"0","end":"10","version":"v4","lat":"12.97159","lng":"77.6056679"},
                                headers={
                                    'Authorization': "Bearer {}".format(constants["access_token"]),
                                    'X-API-Key': "l7xx3e887403b5ed40e78ca8edef65c87587",
                                    'X-CLIENT-TYPE': "myjio"
                                },
                                name="get_coupons")
        print(response)

    def on_start(l):
        """
        on_start is called when a Locust start before,
        any task is scheduled
        """
        l.login_for_access_token()
    @task(1)
    def user_workflow(l):
        sys.stdout.flush()
        l.get_category()
        l.get_favourites()
        l.get_coupons()


class WebsiteUser(HttpLocust):
    min_wait = 1000
    max_wait = 1000
    task_set = UserBehavior
    host = "https:localhost:8083"
