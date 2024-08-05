from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from django.test import Client

from yanews import settings
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def all_news():
    today = timezone.datetime.today()
    all_news = [
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=today - timedelta(days=index)
            )
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comments(news, author):
        now = timezone.now()
        for index in range(10):
            comment = Comment.objects.create(
                news=news, author=author, text=f'Tекст {index}',
            )
            comment.created = now + timedelta(days=index)
            comment.save()


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='text',
    )
    return comment


@pytest.fixture
def id_for_news(news):
    return (news.id,)


@pytest.fixture
def id_for_comment(comment):
    return (comment.id,)


@pytest.fixture
def form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'Новый текст'
    }
