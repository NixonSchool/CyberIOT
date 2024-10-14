"""

This code imports the `AbstractForumProfile` model from the Machina library and
uses `model_factory` to create a concrete `ForumProfile` model based on that
abstract model.

"""
from machina.apps.forum_member.abstract_models import AbstractForumProfile
from machina.core.db.models import model_factory


ForumProfile = model_factory(AbstractForumProfile)
