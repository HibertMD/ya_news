from news.forms import CommentForm
from yanews import settings


def test_news_count(client, all_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, all_news, home_url):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, comments, news_detail_url):
    response = client.get(news_detail_url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_user_has_form(author_client, news, news_detail_url):
    response = author_client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_anonymous_client_has_no_form(client, news, news_detail_url):
    response = client.get(news_detail_url)
    assert 'form' not in response.context
