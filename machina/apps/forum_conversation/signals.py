"""

This code defines a Django signal called topic_viewed,
which can be triggered by the forum application to notify other parts
of the application when a topic is viewed.

"""
import django.dispatch

topic_viewed = django.dispatch.Signal()
