import pytest
from django.conf import settings
from django.urls import reverse
from news.forms import CommentForm

@pytest.mark.usefixtures('news_list')
def test_news_count(client):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.usefixtures('news_list')
def test_news_order(client):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates

@pytest.mark.usefixtures('comment_list')
def test_comments_order(client, comment_list):
    url = reverse('news:detail', args=(comment_list.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps

@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True),
    )
)
def test_comment_form_availability_for_different_users(parametrized_client, form_in_context, news):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    if form_in_context:
        assert 'form' in response.context
        assert isinstance(response.context['form'], CommentForm)
    else:
        assert 'form' not in response.context