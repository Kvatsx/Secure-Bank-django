from django.db import models

class user(models.Model):
    username=models.CharField(max_length=25,primary_key=True)
    password=models.CharField(max_length=20)
    def __str__(self):
        return self.username
    # def __init__(self,a,b):
    #     self.username=a;
        # self.password=b;
    @property
    def getPass(self):
        return self.password