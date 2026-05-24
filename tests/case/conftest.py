"""Pytest 全局基础 fixtures"""
import pytest
from config import BASE_URL


@pytest.fixture(scope="session")
def base_url():
    """被测系统基础 URL"""
    return BASE_URL
