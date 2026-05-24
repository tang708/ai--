"""用户管理模块 fixtures"""
import pytest
from baseAPI.base_api import BaseAPI
from config import TEST_ADMIN, TEST_NORMAL


@pytest.fixture(scope="session")
def admin_session():
    """管理员登录态 — 整个测试运行期间复用"""
    api = BaseAPI()
    resp = api.my_request("POST", "/user/login", json=TEST_ADMIN)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 20000, "管理员登录失败: {}".format(data)
    api.set_token(data["data"]["token"])
    api.token = data["data"]["token"]
    api.user_id = data["data"]["id"]
    api.username = TEST_ADMIN["username"]
    return api


@pytest.fixture(scope="session")
def normal_session():
    """普通用户登录态 — 用于权限校验测试"""
    api = BaseAPI()
    resp = api.my_request("POST", "/user/login", json=TEST_NORMAL)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 20000, "普通用户登录失败: {}".format(data)
    api.set_token(data["data"]["token"])
    api.token = data["data"]["token"]
    api.user_id = data["data"]["id"]
    api.username = TEST_NORMAL["username"]
    return api
