from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """

    @task(4)
    def login(self):
        response = self.client.get("/login")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/login", {"username":"testuser", "password":"password", "next":"/"}, headers={"X-CSRFToken": csrftoken})

    @task(2)
    def go_to_login(self):
        self.client.get("/login")

    @task(2)
    def about(self):
        self.client.get("/about")

    @task(2)
    def see_petmatches(self):
        self.client.get("/#pet-matches")

    @task(3)
    def see_reunited_pets(self):
        self.client.get("/#reunited-pets")

    @task(3)
    def see_activity(self):
        self.client.get("/#activity")                

    @task(8)
    def index(self):
        self.client.get("/")

class WebsiteUser(HttpLocust):
    host = "http://epic-analytics.cs.colorado.edu:8888"
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000