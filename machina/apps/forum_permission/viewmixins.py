"""
    Forum permission view mixins
    ============================

    This module defines permission-related view mixins that can ease the process of verifying forum
    permissions during a view lifetime.

"""

from collections.abc import Iterable
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth.decorators import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url

class PermissionRequiredMixin:
    """ Implements the permissions verification and checks at the view level.

    This view mixin verifies if the current user has the permissions specified by the
    'permission_required' attribute. This 'permissions check' behavior can be updated
    in the 'perform_permissions_check()' method.
    """

    login_url = settings.LOGIN_URL
    permission_required = None
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_required_permissions(self, request):
        """ Returns the required permissions to access the considered object. """
        perms = []

        if not self.permission_required:
            return perms

        if isinstance(self.permission_required, str):
            perms = [self.permission_required, ]
        elif isinstance(self.permission_required, Iterable):
            perms = [perm for perm in self.permission_required]
        else:
            raise ImproperlyConfigured(
                '\'PermissionRequiredMixin\' requires \'permission_required\' '
                'attribute to be set to \'<app_label>.<permission codename>\' but is set to {} '
                'instead'.format(self.permission_required)
            )
        return perms

    def perform_permissions_check(self, user, obj, perms):
        """ Performs the permissions check.

        If no specific permissions are set, the user will be allowed if they are authenticated.
        """
        if not perms:
            # If no permissions are set, skip the check for authenticated users
            return user.is_authenticated

        # Initializes a permission checker if specific permissions are provided
        checker = self.request.forum_permission_handler._get_checker(user)
        # Check permissions
        return all(checker.has_perm(perm, obj) for perm in perms)

    def check_permissions(self, request):
        """ Retrieves the controlled object and performs the permissions check. """
        obj = (
            hasattr(self, 'get_controlled_object') and self.get_controlled_object() or
            hasattr(self, 'get_object') and self.get_object() or getattr(self, 'object', None)
        )
        user = request.user

        # If user is authenticated and no specific permissions are required, allow access
        if user.is_authenticated:
            return None  # Allow access, no need to redirect or raise PermissionDenied

        # Get the permissions to check (if any)
        perms = self.get_required_permissions(self)

        # Check permissions for authenticated users
        has_permissions = self.perform_permissions_check(user, obj, perms)

        if not has_permissions and not user.is_authenticated:
            # Redirect unauthenticated users to the login page
            return HttpResponseRedirect('{}?{}={}'.format(
                resolve_url(self.login_url),
                self.redirect_field_name,
                quote(request.get_full_path())
            ))
        elif not has_permissions:
            raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        """ Dispatches an incoming request. """
        self.request = request
        self.args = args
        self.kwargs = kwargs
        response = self.check_permissions(request)
        if response:
            return response
        return super().dispatch(request, *args, **kwargs)
