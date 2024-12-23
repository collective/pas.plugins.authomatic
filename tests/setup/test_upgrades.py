from pas.plugins.authomatic import PACKAGE_NAME
from Products.GenericSetup.upgrade import listUpgradeSteps

import pytest


@pytest.fixture
def available_steps(portal):
    """Test available steps."""
    setup_tool = portal.portal_setup

    def _match(item, source, dest):
        source, dest = (source,), (dest,)
        return item["source"] == source and item["dest"] == dest

    def func(profile: str, src: str, dst: str):
        steps = listUpgradeSteps(setup_tool, profile, src)
        steps = [s for s in steps if _match(s[0], src, dst)]
        return steps

    return func


class TestUpgrades:
    profile = f"{PACKAGE_NAME}:default"

    @pytest.mark.parametrize("src,dst,expected", [("1", "1000", 1)])
    def test_available(self, available_steps, src, dst, expected):
        steps = available_steps(self.profile, src, dst)
        assert len(steps) == expected
