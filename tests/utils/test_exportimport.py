from pas.plugins.authomatic.useridentities import UserIdentities
from pas.plugins.authomatic.useridentities import UserIdentity
from pas.plugins.authomatic.utils import exportimport

import pytest


IDENTITY = {"provider_name": "github", "id": "42", "email": "a@b.c"}


class TestExportImport:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal
        self.plugin = self.portal.acl_users["authomatic"]

    def _seed(self):
        self.plugin._userid_by_identityinfo[("github", "42")] = "user-1"
        identities = UserIdentities("user-1")
        identities._secret = "sekret"  # noqa: S105
        identities._identities["github"] = UserIdentity.from_dict(IDENTITY)
        self.plugin._useridentities_by_userid["user-1"] = identities

    def test_export(self):
        self._seed()
        data = exportimport._get_plugindata()
        assert data["userid_by_identityinfo"] == {"github|42": "user-1"}
        assert data["useridentities_by_userid"]["user-1"] == {
            "userid": "user-1",
            "secret": "sekret",
            "identities": {"github": IDENTITY},
        }

    def test_roundtrip(self):
        self._seed()
        data = exportimport._get_plugindata()

        # Wipe the plugin state, then import it back.
        self.plugin._init_trees()
        assert exportimport._get_plugindata()["useridentities_by_userid"] == {}
        assert exportimport._set_plugindata(data) is True

        assert dict(self.plugin._userid_by_identityinfo) == {("github", "42"): "user-1"}
        restored = self.plugin._useridentities_by_userid["user-1"]
        assert isinstance(restored, UserIdentities)
        assert restored.secret == "sekret"  # noqa: S105
        assert dict(restored.identity("github")) == IDENTITY

    def test_get_plugindata_without_plugin(self, monkeypatch):
        monkeypatch.setattr(exportimport, "authomatic_plugin", lambda: None)
        assert exportimport._get_plugindata() == {
            "userid_by_identityinfo": {},
            "useridentities_by_userid": {},
        }

    def test_set_plugindata_without_plugin(self, monkeypatch):
        monkeypatch.setattr(exportimport, "authomatic_plugin", lambda: None)
        data = {"userid_by_identityinfo": {}, "useridentities_by_userid": {}}
        assert exportimport._set_plugindata(data) is False

    def test_export_import_plugin_data_file_roundtrip(self, tmp_path):
        self._seed()
        path = tmp_path / "identities.json"

        assert exportimport.export_plugin_data(path) == path
        assert path.exists()

        # Wipe, then import from the file.
        self.plugin._init_trees()
        assert exportimport.import_plugin_data(path) is True

        assert dict(self.plugin._userid_by_identityinfo) == {("github", "42"): "user-1"}
        restored = self.plugin._useridentities_by_userid["user-1"]
        assert restored.secret == "sekret"  # noqa: S105
        assert dict(restored.identity("github")) == IDENTITY
