import pytest
from src.modules.ai_filter import rank_pages

def test_rank_empty():
    assert rank_pages("test", []) == []
