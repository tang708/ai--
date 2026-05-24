"""管理员用户管理 — 数据驱动测试"""
import allure
import pytest
from base_Tool.read_yaml import load_admin_user_data
from base_Tool.db_helper import user_exists, delete_user_by_username
from baseAPI.user_api import UserAPI
from baseAPI.login_api import LoginAPI
from config import TEST_NORMAL


def _admin_query_cases():
    """加载管理员查询相关测试用例"""
    return load_admin_user_data()["test_admin_query"]


def _admin_auth_cases():
    """加载权限校验测试用例"""
    return load_admin_user_data()["test_admin_auth"]


def _case_id(case):
    """取用例 ID 作为 pytest parametrize 的显示名"""
    return case["id"]


@allure.epic("AI健康管理系统")
@allure.feature("管理员-用户管理")
class TestAdminUserQuery:
    """管理员查询测试 — 5 条数据驱动用例"""

    @allure.story("用户查询")
    @pytest.mark.parametrize("case", _admin_query_cases(), ids=_case_id)
    def test_admin_query(self, admin_session, case):
        """数据驱动查询：分页列表/按用户名筛选/全部/按ID/不存在ID"""
        api = UserAPI()
        api.set_token(admin_session.token)
        req = case["request"]
        # 根据 YAML 中的 method 字段动态调用对应的 do_get/do_post/do_put/do_delete
        method = getattr(api, {"GET": "do_get", "POST": "do_post",
                               "PUT": "do_put", "DELETE": "do_delete"}[req["method"]])
        data = method(req["path"], params=req.get("params"), expected_code=None)
        if case["expected"].get("code") is not None:
            assert data.get("code") == case["expected"]["code"]
        if case["expected"].get("code_not") is not None:
            assert data.get("code") != case["expected"]["code_not"]


@allure.epic("AI健康管理系统")
@allure.feature("管理员-用户管理")
class TestAdminUserCRUD:
    """管理员 CRUD 测试 — 新增/重复/修改/删除"""

    NEW_USERNAME = "pytest_admin_test"

    @classmethod
    def teardown_class(cls):
        """测试类结束后清理测试用户"""
        delete_user_by_username(cls.NEW_USERNAME)

    @allure.story("新增用户")
    def test_add_user(self, admin_session):
        """新增用户成功 + 数据库落库验证"""
        api = UserAPI()
        api.set_token(admin_session.token)
        delete_user_by_username(self.NEW_USERNAME)
        data = api.add(self.NEW_USERNAME, "test123456", phone="13900000001",
                       email="admin_test@test.com")
        assert data["code"] == 20000
        assert user_exists(self.NEW_USERNAME)

    @allure.story("新增用户")
    def test_add_duplicate_user(self, admin_session):
        """重复用户名新增必须返回非 20000"""
        api = UserAPI()
        api.set_token(admin_session.token)
        delete_user_by_username(self.NEW_USERNAME)
        api.add(self.NEW_USERNAME, "test123")
        data = api._do("POST", "/user/add", json={
            "username": self.NEW_USERNAME, "password": "test123",
            "phone": "", "email": "", "status": "1"})
        assert data["code"] != 20000

    @allure.story("修改用户")
    def test_update_user(self, admin_session):
        """修改用户手机号成功"""
        api = UserAPI()
        api.set_token(admin_session.token)
        delete_user_by_username(self.NEW_USERNAME)
        api.add(self.NEW_USERNAME, "test123456", phone="13900000001")
        # 从列表中查找新用户的 ID
        list_data = api.get_list(page_no=1, page_size=100)
        uid = None
        for u in list_data.get("data", {}).get("rows", []):
            if u["username"] == self.NEW_USERNAME:
                uid = u["id"]
                break
        assert uid is not None
        data = api.update(uid, self.NEW_USERNAME, phone="13911111111")
        assert data["code"] == 20000

    @allure.story("删除用户")
    def test_delete_user(self, admin_session):
        """删除用户成功（逻辑删，deleted 置 1）"""
        api = UserAPI()
        api.set_token(admin_session.token)
        delete_user_by_username(self.NEW_USERNAME)
        api.add(self.NEW_USERNAME, "test123456", phone="13900000002")
        list_data = api.get_list(page_no=1, page_size=100)
        uid = None
        for u in list_data.get("data", {}).get("rows", []):
            if u["username"] == self.NEW_USERNAME:
                uid = u["id"]
                break
        assert uid is not None
        data = api.delete_user(uid)
        assert data["code"] == 20000


@allure.epic("AI健康管理系统")
@allure.feature("管理员-用户管理")
class TestAdminAuth:
    """权限校验测试 — 管理员/普通用户/无 Token 三种场景"""

    @allure.story("权限校验")
    @pytest.mark.parametrize("case", _admin_auth_cases(), ids=_case_id)
    def test_auth_scenario(self, case, admin_session, normal_session):
        """权限场景测试：根据 YAML 中的 session 字段切换登录态"""
        api = UserAPI()
        if case["session"] == "admin":
            api.set_token(admin_session.token)
        elif case["session"] == "normal":
            api.set_token(normal_session.token)
        # session == "none" 时不设 token，测试未认证访问

        data = api.get_list(page_no=1, page_size=10)
        if case["expected"].get("code") is not None:
            assert data.get("code") == case["expected"]["code"]
        if case["expected"].get("code_not") is not None:
            assert data.get("code") != case["expected"]["code_not"]
