from plone.app.vocabularies import SimpleVocabulary

import pytest


class TestUserIDVocabulary:
    name: str = "pas.plugins.authomatic.userid_vocabulary"
    vocab_type = SimpleVocabulary

    @pytest.fixture(autouse=True)
    def _setup(self, portal_class, get_vocabulary):
        self.portal = portal_class
        self.vocab = get_vocabulary(self.name, self.portal)

    def test_vocabulary_type(self):
        assert isinstance(self.vocab, self.vocab_type)

    @pytest.mark.parametrize(
        "token,title",
        [
            ("uuid", "UUID as User ID"),
            ("userid", "Provider User ID"),
            ("username", "Provider User Name"),
            ("username_userid", "Provider User Name or User ID"),
        ],
    )
    def test_vocab_terms(self, token: str, title: str):
        term = self.vocab.getTermByToken(token)
        assert term.title == title
        assert term.token == token
