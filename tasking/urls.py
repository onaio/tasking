# -*- coding: utf-8 -*-
"""
Tasking urls module.
"""
from django.conf.urls import include, url

from rest_framework import routers

from tasking.viewsets import (ContentTypeViewSet, LocationViewSet,
                              ProjectViewSet, SegmentRuleViewSet,
                              SubmissionViewSet, TaskOccurrenceViewSet,
                              TaskViewSet)

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'contenttypes', ContentTypeViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'segment-rules', SegmentRuleViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'occurrences', TaskOccurrenceViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
