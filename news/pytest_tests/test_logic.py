import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_anonymous_user_cant_create_comment(
        client, news, form_data, news_detail_url
):
    client.post(news_detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author_client, news, form_data, news_detail_url
):
    comments_count_before_post = Comment.objects.count()
    author_client.post(news_detail_url, data=form_data)
    comments_count_after_post = Comment.objects.count()
    assert comments_count_after_post == comments_count_before_post + 1


def test_user_cant_use_bad_words(author_client, news, news_detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'}
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
        author_client, news, comment, comment_delete_url, news_detail_url
):
    response = author_client.get(news_detail_url)
    print(response.context)
    author_client.post(comment_delete_url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


# def test_author_can_edit_comment(author_client, news, comment):
#     NEW_TEXT = 'Новый текст'
#     url = reverse('news:edit', args=(comment.id,))
#     author_client.post(url, data={'text': NEW_TEXT})
#     comment.refresh_from_db()
#     assert comment.text == NEW_TEXT
#
#
# def test_not_author_cant_edit_comment(not_author_client, news, comment):
#     NEW_TEXT = 'Новый текст'
#     url = reverse('news:edit', args=(comment.id,))
#     not_author_client.post(url, data={'text': NEW_TEXT})
#     comment.refresh_from_db()
#     assert comment.text != NEW_TEXT
