from authomatic import Authomatic
from pas.plugins.authomatic.integration import RestAPIAdapter
from pas.plugins.authomatic.utils import authomatic_cfg
from pas.plugins.authomatic.utils import authomatic_settings
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from transaction.interfaces import NoTransaction
from urllib.parse import parse_qsl
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging
import transaction


logger = logging.getLogger("pas.plugins.authomatic")


@implementer(IPublishTraverse)
class LoginAuthomatic(Service):
    """Base class for Authomatic login."""

    AUTHOMATIC_COOKIE = "authomatic"
    provider_id: str = ""
    _providers = None
    _data = None

    def publishTraverse(self, request, name):
        # Store the first path segment as the provider
        request["TraversalRequestNameStack"] = []
        self.provider_id = name
        return self

    @property
    def providers(self) -> dict:
        """Return Authomatic providers."""
        providers = self._providers
        if not providers:
            try:
                providers = authomatic_cfg()
            except KeyError:
                # Authomatic is not configured
                providers = {}
            except ModuleNotFoundError:
                # Bad configuration
                providers = {}
        return providers

    @property
    def json_body(self):
        if not self._data:
            self._data = json_body(self.request)
        return self._data

    @property
    def public_url(self) -> str:
        method = self.request.get("REQUEST_METHOD")
        data = {}
        if method == "GET":
            data = self.request.form
        elif method == "POST":
            data = self.json_body
        public_url = data.get("publicUrl", "")
        if not public_url:
            public_url = api.portal.get().absolute_url()
        return public_url

    def get_auth(self) -> Authomatic:
        providers = self.providers
        secret = authomatic_settings().secret
        return Authomatic(providers, secret=secret)

    def _provider_not_found(self, provider: str) -> dict:
        """Return 404 status code for a provider not found."""
        self.request.response.setStatus(404)
        if not provider:
            message = "Provider was not informed."
        else:
            message = f"Provider {provider} is not available."
        return {
            "error": {
                "type": "Provider not found",
                "message": message,
            }
        }


class Get(LoginAuthomatic):
    """Provide information to start the OAuth process."""

    def extract_cookie_identifier(self, headers: dict) -> str:
        """Get value of Authomatic cookie.

        :param headers: Dictionary with headers set by Authomatic.
        :returns: Value for the cookie set by Authomatic.
        """
        cookie_prefix = f"{self.AUTHOMATIC_COOKIE}="
        value = ""
        cookies = headers.get("Set-Cookie", "").split(";")
        for cookie in cookies:
            if cookie.startswith(cookie_prefix):
                value = cookie.replace(cookie_prefix, "")
        return value

    def reply(self) -> dict:
        """Generate URL and session information to be used by the frontend.

        :returns: URL and session information.
        """
        provider = self.provider_id
        if provider not in self.providers:
            return self._provider_not_found(provider)

        auth = self.get_auth()
        adapter = RestAPIAdapter(self, provider)
        result = auth.login(adapter, provider)
        if result and result.error:
            self.request.response.setStatus(500)
            return {
                "error": {
                    "type": "Configuration error",
                    "message": f"Provider {provider} is not properly configured.",
                }
            }
        else:
            headers = adapter.headers
            identifier = self.extract_cookie_identifier(headers)
            next_url = headers["Location"]
            return {
                "next_url": next_url,
                "session": identifier,
            }


class Post(LoginAuthomatic):
    """Handles OAuth login and returns a JSON web token (JWT)."""

    _aclu = None

    def _get_acl_users(self):
        """Get the acl_users tool.

        :returns: ACL tool.
        """
        if not self._aclu:
            self._aclu = api.portal.get_tool("acl_users")
        return self._aclu

    def _get_jwt_plugin(self):
        """Get the JWT authentication plugin.

        :returns: JWT Authentication plugin.
        """
        aclu = self._get_acl_users()
        plugins = aclu._getOb("plugins")
        authenticators = plugins.listPlugins(IAuthenticationPlugin)
        plugin = None
        for id_, authenticator in authenticators:
            if authenticator.meta_type == "JWT Authentication Plugin":
                plugin = authenticator
                break
        return plugin

    def _add_identity(self, result, userid=None):
        """Add an identity to an existing user.

        :param result: Authomatic login result.
        """
        aclu = self._get_acl_users()
        aclu.authomatic.remember_identity(result, userid)

    def _remember_identity(self, result):
        """Store identity information.

        :param result: Authomatic login result.
        """
        aclu = self._get_acl_users()
        aclu.authomatic.remember(result)

    def get_token(self, user) -> str:
        """Generate JWT token for user.

        :param user: User memberdata.
        :returns: JWT token.
        """
        token = ""
        plugin = self._get_jwt_plugin()
        if plugin:
            payload = {"fullname": user.getProperty("fullname")}
            token = plugin.create_token(user.getId(), data=payload)
        return token

    def _annotate_transaction(self, action, user):
        """Add a note to the current transaction."""
        try:
            # Get the current transaction
            tx = transaction.get()
        except NoTransaction:
            return None
        # Set user on the transaction
        tx.setUser(user.getUser())
        user_info = user.getProperty("fullname") or user.getUserName()
        msg = ""
        if action == "login":
            msg = f"(Logged in {user_info})"
        elif action == "add_identity":
            msg = f"(Added new identity to user {user_info})"
        tx.note(msg)

    def reply(self) -> dict:
        """Process OAuth callback, authenticate the user and return a JWT Token.

        :returns: Token information.
        """
        provider = self.provider_id
        if provider not in self.providers:
            return self._provider_not_found(provider)

        data = self.json_body
        qs = data.get("qs", "")
        if qs.startswith("?"):
            qs = qs[1:]
        qs = dict(parse_qsl(qs))
        cookies = {self.AUTHOMATIC_COOKIE: data.get("session", "")}
        adapter = RestAPIAdapter(self, provider, qs, cookies)
        auth = self.get_auth()
        result = auth.login(adapter, provider)
        if result and result.error:
            self.request.response.setStatus(401)
            return {
                "error": {
                    "type": "Authentication Error",
                    "message": f"{result.error}",
                }
            }
        elif result:
            alsoProvides(self.request, IDisableCSRFProtection)
            action = ""
            if api.user.is_anonymous():
                self._remember_identity(result)
                action = "login"
            else:
                # Authenticated user, add an identity to it
                try:
                    userid = api.user.get_current().getId()
                    self._add_identity(result, userid)
                    action = "add_identity"
                except ValueError as err:
                    logger.exception(err)

            user = api.user.get_current()
            # Make sure we are not setting cookies here
            # as it will break the authentication mechanism with JWT tokens
            self.request.response.cookies = {}
            if action:
                self._annotate_transaction(action, user=user)
            return {"token": self.get_token(user)}
