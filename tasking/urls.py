# -*- coding: utf-8 -*-
"""
Tasking urls module.
"""
from django.conf.urls import include, url

from rest_framework import routers

from tasking.viewsets import (LocationViewSet, ProjectViewSet,
                              SegmentRuleViewSet, SubmissionViewSet,
                              TaskViewSet, ContentTypeViewSet)

# pylint: disable=invalid-name
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'segment-rules', SegmentRuleViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'contenttypes', ContentTypeViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
]
