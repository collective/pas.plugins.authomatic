from authomatic.core import Credentials
from pas.plugins.authomatic._types import AuthResult
from pas.plugins.authomatic._types import ProviderConfig
from pas.plugins.authomatic.utils import authomatic_cfg
from persistent import Persistent
from persistent.mapping import PersistentMapping
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet
from typing import Any

import uuid


class UserIdentity(PersistentMapping):
    data: dict

    def __init__(self, result: AuthResult) -> None:
        super().__init__()
        self["provider_name"] = result.provider.name
        self.update(result.user.to_dict())

    @property
    def credentials(self) -> Credentials:
        cfg = authomatic_cfg()
        return Credentials.deserialize(cfg, self.user["credentials"])

    @credentials.setter
    def credentials(self, credentials: Credentials) -> None:
        self.data["credentials"] = credentials.serialize()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserIdentity":
        """Reconstruct a :class:`UserIdentity` from its serialized mapping.

        Bypasses ``__init__`` (which expects an Authomatic result) so an
        identity can be rebuilt from exported data.

        :param data: Mapping previously produced by ``dict(identity)``.
        :returns: The reconstructed identity.
        """
        identity = cls.__new__(cls)
        PersistentMapping.__init__(identity)
        identity.update(data)
        return identity


class UserIdentities(Persistent):
    userid: str
    _identities: PersistentMapping
    _sheet: UserPropertySheet | None
    _secret: str

    def __init__(self, userid: str) -> None:
        self.userid = userid
        self._identities = PersistentMapping()
        self._sheet = None
        self._secret = str(uuid.uuid4())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserIdentities":
        """Reconstruct a :class:`UserIdentities` from its serialized form.

        :param data: Mapping with ``userid``, ``secret`` and ``identities``
            keys, as produced during export.
        :returns: The reconstructed user identities.
        """
        instance = cls(data["userid"])
        instance._secret = data["secret"]
        for provider, identity_data in data["identities"].items():
            instance._identities[provider] = UserIdentity.from_dict(identity_data)
        return instance

    @property
    def secret(self) -> str:
        return self._secret

    def check_password(self, password: str) -> bool:
        return password == self._secret

    def handle_result(self, result: AuthResult) -> None:
        """add a authomatic result to this user"""
        self._sheet = None  # invalidate property sheet
        self._identities[result.provider.name] = UserIdentity(result)

    def identity(self, provider: str) -> UserIdentity | None:
        """users identity at a distinct provider"""
        return self._identities.get(provider, None)

    def update_userdata(self, result: AuthResult) -> None:
        self._sheet = None  # invalidate property sheet
        identity = self._identities[result.provider.name]
        identity.update(result.user.to_dict())

    def _properties_from_identity(
        self, identity: UserIdentity, cfg: ProviderConfig
    ) -> dict[str, Any]:
        """return the property for a given identity"""
        pdata = {}
        for akey, pkey in cfg.get("propertymap", {}).items():
            # Always search first on the user attributes, then on the raw
            # data this guaratees we do not break existing configurations
            ainfo = identity.get(akey, None) or identity["data"].get(akey, None)
            if ainfo is None:
                continue
            if isinstance(pkey, dict):
                for k, v in pkey.items():
                    pdata[k] = ainfo.get(v)
            else:
                pdata[pkey] = ainfo
        return pdata

    def _prepare_property_sheet(self) -> dict[str, Any]:
        """build a property sheet from the identities"""
        pdata = {"id": self.userid}
        if cfgs_providers := authomatic_cfg():
            for provider_name, cfg in cfgs_providers.items():
                identity = self.identity(provider_name)
                if identity is None:
                    continue
                pdata.update(self._properties_from_identity(identity, cfg))
        return pdata

    @property
    def propertysheet(self) -> UserPropertySheet:
        if self._sheet is not None:
            return self._sheet
        # build sheet from identities
        pdata = self._prepare_property_sheet()
        self._sheet = UserPropertySheet(**pdata)
        return self._sheet
