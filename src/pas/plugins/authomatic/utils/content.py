from plone.base.interfaces.siteroot import INavigationRoot
from plone.dexterity.content import DexterityContent
from Products.CMFCore.interfaces import ISiteRoot


def is_root(obj: DexterityContent) -> bool:
    """Check if current context is Navigation root or a Portal."""
    return ISiteRoot.providedBy(obj) or INavigationRoot.providedBy(obj)
