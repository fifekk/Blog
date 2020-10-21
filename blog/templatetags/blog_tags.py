from django import template
from django.db.models import Count

from ..models import Post

# this variable have to occur always with templatetags
register = template.Library()

# simple_tag processes the data and returns a string

@register.simple_tag
def total_posts():
    """
    Simple tag that returns number of published posts
    Tag name is total_post.
    If you want to change name to another use @register.simple_tag(name='tag_name')
    """
    return Post.published.count()


# insclusion_tag gives us possibility to render a template with context variables returned by template tag


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    return latest_posts template with context variable that contains
    latest 5 posts (or more, depends on counte arg)
    you can specify number of posts in template just use:
    {% show_latest_posts 3 %}
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


