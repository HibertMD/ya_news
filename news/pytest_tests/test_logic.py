from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_user_cant_use_bad_words(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, news, comment):
    url = reverse('news:delete', args=(comment.id,))
    author_client.post(url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, news, comment):
    NEW_TEXT = 'Новый текст'
    url = reverse('news:edit', args=(comment.id,))
    author_client.post(url, data={'text': NEW_TEXT})
    comment.refresh_from_db()
    assert comment.text == NEW_TEXT


def test_author_can_edit_comment(not_author_client, news, comment):
    NEW_TEXT = 'Новый текст'
    url = reverse('news:edit', args=(comment.id,))
    not_author_client.post(url, data={'text': NEW_TEXT})
    comment.refresh_from_db()
    assert comment.text != NEW_TEXT
