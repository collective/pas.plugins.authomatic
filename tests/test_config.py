from pas.plugins.authomatic.config import DEFAULT_CONFIG
from pas.plugins.authomatic.config import validate_cfg_json
from zope.interface import Invalid

import pytest


class TestValidateCfgJson:
    def test_valid_default_config(self):
        assert validate_cfg_json(DEFAULT_CONFIG) is True

    def test_valid_minimal_config(self):
        assert validate_cfg_json('{"github": {}}') is True

    def test_invalid_json_raises(self):
        with pytest.raises(Invalid):
            validate_cfg_json("{not valid json")

    def test_non_mapping_raises(self):
        with pytest.raises(Invalid):
            validate_cfg_json("[1, 2, 3]")

    def test_empty_mapping_raises(self):
        with pytest.raises(Invalid):
            validate_cfg_json("{}")
