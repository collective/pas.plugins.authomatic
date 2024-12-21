from Products.PluggableAuthService.UserPropertySheet import UserPropertySheet

import pytest


@pytest.fixture
def authomatic_user_factory(mock_result):
    from authomatic.core import User

    def func(provider_name="MockPlone", data=None, props=None):
        props = props if props else {}
        provider = mock_result(name=provider_name)
        if not data:
            data = {
                "displayName": "Andrew Pipkin",
                "domain": "foobar.com",
                "emails": [{"type": "account", "value": "andrewpipkin@foobar.com"}],
                "etag": '"xxxxxxxxxxxx/xxxxxxxxxxxx"',
                "id": "123456789",
                "image": {
                    "isDefault": False,
                    "url": "https://lh3.googleusercontent.com/photo.jpg",
                },
                "isPlusUser": False,
                "kind": "plus#person",
                "language": "en_GB",
                "name": {"familyName": "Pipkin", "givenName": "Andrew"},
                "objectType": "person",
                "verified": False,
            }
        user = User(provider)
        user.data = data
        user.id = "123456789"
        user.username = "andrewpipkin"
        user.name = "Andrew Pipkin"
        user.first_name = "Andrew"
        user.last_name = "Pipkin"
        user.nickname = "Andy"
        user.link = "http://peterhudec.github.io/authomatic/"
        user.email = "andrewpipkin@foobar.com"
        user.picture = "https://lh3.googleusercontent.com/photo.jpg?sz=50"
        user.location = "Innsbruck"
        for prop in props:
            setattr(user, prop, props[prop])
        return user

    return func


@pytest.fixture
def one_user(make_user, mock_result, authomatic_user_factory):
    def func(plugin, provider_name, data=None, props=None):
        data = data if data else {}
        props = props if props else {}
        user = make_user("mustermann", plugin=plugin)
        authomatic_result = mock_result(
            user=authomatic_user_factory(
                provider_name=provider_name, data=data, props=props
            ),
            provider=mock_result(name=provider_name),
        )
        user.handle_result(authomatic_result)
        return user

    return func


@pytest.fixture
def patch_authomatic(monkeypatch):
    def func(provider_name: str = "mockhub", custom_props: dict | None = None):
        from pas.plugins.authomatic import useridentities

        def authomatic_cfg():
            proppropertymap = {
                "email": "email",
                "link": "home_page",
                "location": "location",
                "name": "fullname",
            }
            if custom_props:
                proppropertymap.update(custom_props)
            return {provider_name: {"propertymap": proppropertymap}}

        monkeypatch.setattr(useridentities, "authomatic_cfg", authomatic_cfg)

    return func


class TestUserIdentity:
    @pytest.fixture(autouse=True)
    def _set_up(self, mock_result):
        self.input_name = "mockprovider"
        self.result = mock_result(
            provider=mock_result(name=self.input_name),
            user=mock_result(),
        )

    def test_init(self):
        from pas.plugins.authomatic.useridentities import UserIdentity

        ui = UserIdentity(self.result)
        assert self.input_name == ui["provider_name"]


class TestUserIdentities:
    provider_name: str = "mockhub"

    @pytest.fixture(autouse=True)
    def _set_up(self, plugin, patch_authomatic, one_user):
        self.plugin = plugin
        patch_authomatic(self.provider_name)
        self.user = one_user(plugin, self.provider_name, data={})

    def test_identities_init(self):
        input_userid = "mockuserid"
        from pas.plugins.authomatic.useridentities import UserIdentities

        uis = UserIdentities(input_userid)
        assert uis.userid == input_userid

    def test_sheet_existing_user(self):
        sheet = self.user.propertysheet
        assert isinstance(sheet, UserPropertySheet)

    @pytest.mark.parametrize(
        "prop_name, expected",
        [
            ["home_page", "http://peterhudec.github.io/authomatic/"],
            ["fullname", "Andrew Pipkin"],
            ["email", "andrewpipkin@foobar.com"],
        ],
    )
    def test_sheet_existing_user_attributes(self, prop_name, expected):
        sheet = self.user.propertysheet
        assert sheet.getProperty(prop_name) == expected

    def test_read_attribute_from_provider_data_if_default_is_none(self, one_user):
        user = one_user(
            self.plugin,
            self.provider_name,
            data={"email": "jdoe@foobar.com"},
            props={"email": None},
        )
        sheet = user.propertysheet
        assert sheet.getProperty("email") == "jdoe@foobar.com"


class TestUserIdentitiesCustomProps:
    provider_name: str = "mockhub"

    @pytest.fixture(autouse=True)
    def _set_up(self, plugin, patch_authomatic, one_user):
        self.plugin = plugin
        custom_props = {"domain": "customdomain"}
        patch_authomatic(self.provider_name, custom_props=custom_props)
        self.user = one_user(plugin, self.provider_name, data={})

    @pytest.mark.parametrize(
        "prop_name, expected",
        [
            ["home_page", "http://peterhudec.github.io/authomatic/"],
            ["fullname", "Andrew Pipkin"],
            ["email", "andrewpipkin@foobar.com"],
            ["customdomain", "foobar.com"],
        ],
    )
    def test_sheet_user_attributes(self, prop_name, expected):
        sheet = self.user.propertysheet
        assert sheet.getProperty(prop_name) == expected
