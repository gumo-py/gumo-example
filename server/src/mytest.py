import pytest
import main

main.app.testing = True
client = main.app.test_client()

__all__ = [
    'pytest',
    'client',
]
