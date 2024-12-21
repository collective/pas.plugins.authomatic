import pytest


@pytest.fixture
def populate_users(make_user):
    def func(plugin):
        logins = [
            "123joe",
            "123jane",
            "123wily",
            "123willi",
        ]
        for login in logins:
            make_user(login, plugin)

    return func


@pytest.fixture
def populate_admins(portal, plugin, make_user):
    aclu = portal.acl_users
    aclu.userFolderAddUser("admin", "admin", [], [])  # zope admin
    make_user("administrator", plugin=plugin)  # oauth administrator


class TestPlugin:
    @pytest.fixture(autouse=True)
    def _set_up(self, portal, plugin):
        self.aclu = portal.acl_users
        self.plugin = plugin

    def test_user_enumeration_empty_query(self, populate_users):
        populate_users(self.plugin)
        # https://github.com/collective/pas.plugins.authomatic/pull/25/commits/5c0f6b1dc76a0d769e35a845ce4c4dd4307655ba
        # Due to the workarround, now the enumerateUsers plugin doesn't return
        # any users when searching with an empty query
        assert len(self.plugin.enumerateUsers()) == 0

    @pytest.mark.parametrize(
        "query,expected",
        [
            ["123", 4],
            ["123j", 2],
            ["123jo", 1],
            ["123w", 2],
            ["user", 0],
        ],
    )
    def test_user_enumeration_not_exact_match(self, populate_users, query, expected):
        populate_users(self.plugin)
        # check by user id
        result = self.plugin.enumerateUsers(id=query)
        assert len(result) == expected

    @pytest.mark.parametrize(
        "login",
        [
            "123joe",
            "123jane",
            "123wily",
            "123willi",
        ],
    )
    def test_user_enumeration(self, make_user, login):
        make_user(login, plugin=self.plugin)
        # check by user id
        result = self.plugin.enumerateUsers(id=login, exact_match=True)
        assert len(result) == 1
        assert result[0] == {"login": login, "pluginid": "authomatic", "id": login}

    def test_user_delete(self, populate_users):
        populate_users(self.plugin)
        assert len(self.plugin.enumerateUsers(login="123j")) == 2
        assert len(self.plugin.enumerateUsers(login="123joe")) == 1
        self.plugin.doDeleteUser(userid="123joe")
        assert len(self.plugin.enumerateUsers(login="123j")) == 1
        assert len(self.plugin.enumerateUsers(login="123joe")) == 0

    def test_user_delete_invalid_uid(self, populate_users):
        populate_users(self.plugin)
        assert len(self.plugin.enumerateUsers(login="123j")) == 2
        self.plugin.doDeleteUser(userid="123foo")
        assert len(self.plugin.enumerateUsers(login="123j")) == 2

    def test_authentication_empty_deny(self):
        credentials = {}
        result = self.plugin.authenticateCredentials(credentials)
        assert result is None

    def test_authentication_nonexistent_deny(self):
        credentials = {
            "login": "UNSET",
            "password": "UNSET",
        }
        result = self.plugin.authenticateCredentials(credentials)
        assert result is None

    def test_authentication_user_no_pass_deny(self, make_user):
        make_user("joe", plugin=self.plugin)
        credentials = {
            "login": "joe",
            "password": "SECRET",
        }
        result = self.plugin.authenticateCredentials(credentials)
        assert result is None

    def test_authentication_user_same_pass_allow(self, make_user):
        make_user("joe", plugin=self.plugin, password="SECRET")  # noQA: S106
        credentials = {"login": "joe", "password": "SECRET"}
        result = self.plugin.authenticateCredentials(credentials)
        assert result == ("joe", "joe")

    def test_admin_search_exact_match(self, populate_admins):
        # check searching exact user by plugins: authomatic and ZODBUserManager
        assert len(self.aclu.searchUsers(id="adm", exact_match=True)) == 0

    @pytest.mark.parametrize(
        "userid,expected_plugin_id",
        [
            ("administrator", "authomatic"),
            ("admin", "source_users"),
        ],
    )
    def test_authentication_zope_admin(
        self, populate_admins, userid, expected_plugin_id
    ):
        user = self.aclu.searchUsers(id=userid, exact_match=True)[0]
        assert user["pluginid"] == expected_plugin_id
