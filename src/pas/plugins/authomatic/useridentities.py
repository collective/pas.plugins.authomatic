from authomatic.core import Credentials
from pas.plugins.authomatic.utils import authomatic_cfg
from persistent import Persistent
from persistent.dict import PersistentDict
from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet

import logging
import uuid


logger = logging.getLogger("pas.plugins.authomatic")


class UserIdentity(PersistentDict):
    def __init__(self, result):
        super().__init__()
        self["provider_name"] = result.provider.name
        self.update(result.user.to_dict())

    @property
    def credentials(self):
        cfg = authomatic_cfg()
        return Credentials.deserialize(cfg, self.user["credentials"])

    @credentials.setter
    def credentials(self, credentials):
        self.data["credentials"] = credentials.serialize()


class UserIdentities(Persistent):
    def __init__(self, userid):
        self.userid = userid
        self._identities = PersistentDict()
        self._sheet = None
        self._secret = str(uuid.uuid4())

    @property
    def secret(self):
        return self._secret

    def check_password(self, password):
        return password == self._secret

    def handle_result(self, result):
        """add a authomatic result to this user"""
        self._sheet = None  # invalidate property sheet
        self._identities[result.provider.name] = UserIdentity(result)

    def identity(self, provider):
        """users identity at a distinct provider"""
        return self._identities.get(provider, None)

    def update_userdata(self, result):
        self._sheet = None  # invalidate property sheet
        identity = self._identities[result.provider.name]
        identity.update(result.user.to_dict())

    @property
    def propertysheet(self):
        if self._sheet is not None:
            return self._sheet
        # build sheet from identities
        pdata = dict(id=self.userid)
        cfgs_providers = authomatic_cfg()
        for provider_name in cfgs_providers:
            identity = self.identity(provider_name)
            if identity is None:
                continue
            logger.debug(identity)
            cfg = cfgs_providers[provider_name]
            for akey, pkey in cfg.get("propertymap", {}).items():
                # Always search first on the user attributes, then on the raw
                # data this guaratees we do not break existing configurations
                ainfo = identity.get(akey, identity["data"].get(akey, None))
                if ainfo is None:
                    continue
                if isinstance(pkey, dict):
                    for k, v in pkey.items():
                        pdata[k] = ainfo.get(v)
                else:
                    pdata[pkey] = ainfo
        self._sheet = UserPropertySheet(**pdata)
        return self._sheet
