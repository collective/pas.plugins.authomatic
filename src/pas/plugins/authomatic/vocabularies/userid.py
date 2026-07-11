from pas.plugins.authomatic.interfaces import IUserIDFactory
from plone.dexterity.content import DexterityContent
from zope.component import getUtilitiesFor
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def userid_factory_vocabulary(context: DexterityContent) -> SimpleVocabulary:
    """Vocabulary of the registered user id factories."""
    items = []
    for name, factory in getUtilitiesFor(IUserIDFactory):
        items.append([factory.title, name])
    terms = [SimpleTerm(name, name, title) for title, name in sorted(items)]
    return SimpleVocabulary(terms)
