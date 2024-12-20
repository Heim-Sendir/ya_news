from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.models import Comment
from news.forms import WARNING, BAD_WORDS


def test_user_can_create_comment(
    author_client, news, form_data_comment, pk_for_news
):
    url = reverse('news:detail', args=pk_for_news)
    url_to_comment = url + '#comments'
    comment_count = Comment.objects.count()
    response = author_client.post(url_to_comment, data=form_data_comment)
    assertRedirects(response, url_to_comment)
    news.refresh_from_db()
    assert Comment.objects.count() == comment_count + 1


def test_anoymous_user_cant_create_comment(
    client, news, form_data_comment, pk_for_news
):
    url = reverse('news:detail', args=pk_for_news)
    url_to_comment = url + '#comments'
    comment_count = Comment.objects.count()
    response = client.post(url_to_comment, data=form_data_comment)
    login_url = reverse('users:login')
    excepted_url = f'{login_url}?next={url}'
    assertRedirects(response, excepted_url)
    news.refresh_from_db()
    assert Comment.objects.count() == comment_count


def test_user_can_edit_comment(
    author_client, news, comment, form_data_comment,
    pk_for_comment, pk_for_news
):
    url = reverse('news:edit', args=pk_for_comment)
    url_to_comment = reverse('news:detail', args=pk_for_news) + '#comments'
    response = author_client.post(url, data=form_data_comment)
    assertRedirects(response, url_to_comment)
    comment.refresh_from_db()
    assert comment.text == form_data_comment['text']


def test_another_user_cant_edit_comment(
    not_author_client,
    form_data_comment, pk_for_comment
):
    url = reverse('news:edit', args=pk_for_comment)
    response = not_author_client.post(url, data=form_data_comment)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_can_delete_comment(
    author_client, pk_for_comment, pk_for_news
):
    url = reverse('news:delete', args=pk_for_comment)
    url_to_comment = reverse('news:detail', args=pk_for_news) + '#comments'
    response = author_client.post(url)
    assertRedirects(response, url_to_comment)
    assert Comment.objects.count() == 0


def test_another_user_cant_delete_comment(
    not_author_client, pk_for_comment
):
    url = reverse('news:delete', args=pk_for_comment)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_comment_form_on_forbiden_words(
    author_client, form_data_comment, pk_for_news
):
    url = reverse('news:detail', args=pk_for_news)
    for word in BAD_WORDS:
        form_data_comment['text'] = word
        response = author_client.post(url, data=form_data_comment)
        assertFormError(response, 'form', 'text', WARNING)
