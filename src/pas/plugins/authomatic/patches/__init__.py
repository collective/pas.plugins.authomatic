def apply_patches():
    """Apply patches."""
    from .authomatic import patch_base_provider_fetch

    patch_base_provider_fetch()
