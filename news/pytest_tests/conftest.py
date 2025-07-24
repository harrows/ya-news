import pytest
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.utils import timezone
from news.models import Comment, News

User = get_user_model()

@pytest.fixture
def author():
    return User.objects.create(username='Автор')

@pytest.fixture
def reader():
    return User.objects.create(username='Читатель')

@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client

@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client

@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')

@pytest.fixture
def comment(author, news):
    return Comment.objects.create(news=news, author=author, text='Текст комментария')

@pytest.fixture
def id_for_args(news):
    return (news.id,)

@pytest.fixture
def comment_id_for_args(comment):
    return (comment.id,)

@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}

@pytest.fixture
def news_list():
    today = timezone.now()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )

@pytest.fixture
def comment_list(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news