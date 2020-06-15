from faker import Faker

from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class Board(models.Model):
    name = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100)
    auth_required = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def init(cls):
        board_data = [
            {
                'name': '공지사항',
                'url_name': 'notice',
                'auth_required': True,
            },
            {
                'name': '자유게시판',
                'url_name': 'free',
            },
            {
                'name': '추천게시판',
                'url_name': 'recommend',
            },
        ]
        for board in board_data:
            Board.objects.create(**board)
        

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    hits = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

    def hit(self):
        self.hits += 1
        self.save()

    def dummy(count):
        faker = Faker('ko-KR')
        if Board.objects.count() == 0:
            Board.objects.create(name="testboard")
        if get_user_model().objects.count() == 0:
            get_user_model().objects.create(
                username=faker.name(),
                password="1"
            )
        for _ in range(count):
            Article.objects.create(
                title=faker.sentence(),
                content=str(faker.text()) * 10,
                author=get_user_model().objects.get(pk=1),
                board=Board.objects.get(pk=3)
            )

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
