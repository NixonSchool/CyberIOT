from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from .models import Post

class LatestPostsFeed(Feed):
    title = "My blog"
    link = "/feeds/latest/"
    description = "New posts of my blog."

    def items(self):
        return Post.objects.filter(status=1).order_by("-created_on")  # Order by latest posts

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

    def item_link(self, item):
        return reverse("post_detail", args=[item.slug])  # Ensure you have the correct URL pattern for this, if not, django will report you to your police station.

class AtomSiteNewsFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
