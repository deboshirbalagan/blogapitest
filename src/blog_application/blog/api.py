import datetime
from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer
from restless.exceptions import NotFound

from django.db.models import Q
from .models import User, Post


class APIFilterMixin:
    allowed_fields_filter = []

    def filter(self, queryset):
        filters = {}
        for arg in self.request.GET:
            if arg in self.allowed_fields_filter:
                filters.update({arg: self.request.GET.get(arg)})
        return queryset.filter(**filters)

class APIOrderingMixin:
    allowed_fields_ordering = []
    ordering_field = 'order_by'

    def ordering(self, queryset):
        order_by = self.request.GET.get(self.ordering_field)
        if not order_by:
            return queryset

        if order_by.split('-')[-1] in self.allowed_fields_ordering:
            return queryset.order_by(order_by)

        return queryset

class PostResource(APIFilterMixin, APIOrderingMixin, DjangoResource):


    preparer = FieldsPreparer(fields={
        'text': 'text',
        'created_at': 'created_at',
        'author': 'author.username',
        'likes': 'likes',
    })

    allowed_fields_filter = [
        'text', 'text__icontains', 'text__startswith', 'author', 'likes__lt',
        'likes__gt']

    allowed_fields_ordering = ['likes', 'created_at']

    def is_authenticated(self):
        return True

    def list(self):

        return self.ordering(self.filter(Post.objects.all()))

    def detail(self, pk):

        return Post.objects.get(id=pk)

    def create(self):

        return Post.objects.create(

            text=self.data['text'],
            created_at = datetime.datetime.now(),
            author = User.objects.get(username = self.data['author']),

        )

    def update(self, pk):

        try:
            post = Post.objects.get(id=pk)

        except Post.DoesNotExist:
            post = Post()

        post.text = self.data['text']
        post.author = User.objects.get(username=self.data['author'])
        post.likes = self.data['likes']
        post.created_at = datetime.datetime.now()
        post.save()

        return post


    def delete(self, pk):

        Post.objects.get(id=pk).delete()


class UserResource(APIFilterMixin, APIOrderingMixin, DjangoResource):


    preparer = FieldsPreparer(fields={
        'username': 'username',
        'about': 'about',
        'friends': 'get_all_friends'
    })

    allowed_fields_filter = [
        'username', 'username__icontains', 'username__startswith', 'about__icontains', ]

    allowed_fields_ordering = ['username']

    def list(self):
        return self.ordering(self.filter(User.objects.all()))

    def is_authenticated(self):
        return True

    def detail(self, pk):

        return User.objects.get(id=pk)



    def create(self):

        user = User.objects.create(

            username=self.data['username'],
            about = self.data['about']


        )
        user.friends.set([User.objects.get(username=friend) for friend in self.data['friends']])

        return user

    def update(self, pk):

        try:
            user = User.objects.get(id=pk)

        except User.DoesNotExist:

            user = User()

        user.username = self.data['username']
        user.about = self.data['about']
        user.save()
        user.friends.set([User.objects.get(username=friend) for friend in self.data['friends']])


        return user

    def delete(self, pk):

        User.objects.get(id=pk).delete()