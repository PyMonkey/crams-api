# coding=utf-8
"""
    URL definitions
"""

from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
# from rest_framework.authtoken import views
from crams.views import debug_add_approver_role, debug_add_provisioner_role

from crams.api.v1.views import RequestViewSet, ContactViewSet, ContactDetail, \
    ProjectViewSet, ApproveRequestViewSet, DeclineRequestViewSet, \
    SearchContact, ProvisionRequestViewSet, ProvisionProjectViewSet, \
    UpdateProvisionProjectViewSet

from crams.api.v1.auth import CramsLoginAuthToken

from crams.api.v1.views_list import CurrentUserApproverRoleList, \
    RequestHistoryViewSet, CurrentUserRolesView
from crams.api.v1 import lookup, auth
from crams.api.v1.projectRequestListAPI import \
     ApproverReviewerRequestListView, \
     UserProjectListView, \
     UserProjectRequestListView, \
     FundingBodyAllocationsCounter


router = routers.SimpleRouter()
router.register(r'project', ProjectViewSet)
router.register(r'request_history', RequestHistoryViewSet, base_name='history')
router.register(r'request', RequestViewSet)
router.register(r'approve_request', ApproveRequestViewSet)
router.register(r'decline_request', DeclineRequestViewSet)
router.register(r'provision_project/list', ProvisionProjectViewSet)
router.register(r'provision_project/update', UpdateProvisionProjectViewSet)
router.register(r'provision_request/list', ProvisionRequestViewSet)
router.register(r'user_funding_body',
                CurrentUserApproverRoleList, base_name='funding_body')
router.register(r'contact', ContactViewSet)


urlpatterns = [
    url(r'^accounts/auth/$', CramsLoginAuthToken.as_view()),
    url(r'^', include(router.urls, namespace='crams')),
    url(r'set_tokens', auth.set_tokens),
    url(r'api-token-auth', CramsLoginAuthToken.as_view()),
    url(r'redirect-to-rc-shib', auth.redirect_to_rc_shib),
    url(r'user_roles', CurrentUserRolesView.as_view()),
    url(r'alloc_home', lookup.allocation_home),
    url(r'durations', lookup.durations),
    url(r'grant_types', lookup.grant_types),
    url(r'for_codes', lookup.for_codes),
    # Storage Products
    url(r'nectar_sps', lookup.fb_storage_product, {'searchKey': 'NeCTAR'}),
    url(r'vicnode_sps', lookup.fb_storage_product, {'searchKey': 'VicNode'}),

    url(r'contacts', lookup.contacts),
    url(r'^contact/(?P<email>[\w.@+-]+)/$', ContactDetail.as_view()),
    url(r'searchcontact', SearchContact.as_view()),
    url(r'project_list', UserProjectListView.as_view()),
    url(r'project_request_list', UserProjectRequestListView.as_view()),
    url(r'approve_list', ApproverReviewerRequestListView.as_view()),
    url(r'alloc_counter', FundingBodyAllocationsCounter.as_view()),
]

if settings.DEBUG:
    urlpatterns += url(r'debug_add_approver_role/(?P<fb_name>[\w]+)',
                       debug_add_approver_role),
    urlpatterns += url(r'debug_add_provisioner_role',
                       debug_add_provisioner_role),
