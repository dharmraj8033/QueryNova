import pytest
from src.modules.search import search

def test_search_returns_list():
    results = search("test")
    assert isinstance(results, list)
    # Without valid API key, may be empty but should not error
