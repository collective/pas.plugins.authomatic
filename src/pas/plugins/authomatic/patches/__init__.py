from logging import Logger


def apply_patches(logger: Logger):
    """Apply patches."""
    from .authomatic import patch_base_provider_fetch

    patch_base_provider_fetch(logger)
