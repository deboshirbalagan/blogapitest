from django.db import models


class User(models.Model):

    username = models.CharField(unique=True, max_length=50)
    about = models.TextField()
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):

        return self.username

    def get_all_friends(self):

        q = self.friends.all()
        friends_list = [friend.username for friend in q]

        return friends_list

class Post(models.Model):

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

