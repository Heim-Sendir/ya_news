import pytest

from django.test.client import Client

from news.models import Comment, News


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
    print(client)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Комментарий',
    )
    return comment


@pytest.fixture
def pk_for_news(news):
    return (news.pk,)


@pytest.fixture
def pk_for_comment(comment):
    return (comment.pk,)


@pytest.fixture
def pk_for_news(news):
    return (news.pk,)


@pytest.fixture
def form_data_comment():
    return {
        'text': 'Изменённый комментарий'
    }
