class MockResult(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def to_dict(self):
        return self


class MockCredentials(MockResult):
    def refresh(*args):
        pass


def make_user(login, testcase=None, password=None):
    from pas.plugins.authomatic.useridentities import UserIdentities

    uis = UserIdentities(login)
    if password:
        uis._secret = password
    if testcase:
        testcase.plugin._useridentities_by_userid[login] = uis
    mock_result = MockResult(
        provider=MockResult(name="mock_provider"), user=MockResult()
    )
    uis.handle_result(mock_result)
    return uis
