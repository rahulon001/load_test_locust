# from locust import TaskSet, task
#
# def login(l):
#     l.client.post("/jm/auth/oauth/v2/token", {"username":"9945240311", "password":"jiomoney@2"})
#     return
#
# # def make_echo_request(l):
# #     l.client.get("/cr/v2/coupons/category",)
# #
# # def profile(l):
# #     l.client.get("/profile")
#
#
# class MyTask(TaskSet):
#     # tasks = {make_echo_request: 2, profile: 1}
#     def on_start(self):
#         login(self)
