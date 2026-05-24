"""登录注册模块 — 数据驱动测试"""
import allure
import pytest
from base_Tool.read_yaml import load_login_data, load_register_data
from base_Tool.db_helper import user_exists, delete_user_by_username
from baseAPI.login_api import LoginAPI
from config import TEST_ADMIN, TEST_NORMAL


def _get_login_cases():
    """从 YAML 加载登录用例，传入 context 解析 ${TEST_ADMIN.username} 等占位符"""
    ctx = {"TEST_ADMIN": TEST_ADMIN, "TEST_NORMAL": TEST_NORMAL}
    return load_login_data(ctx)["test_login"]


def _get_register_cases():
    """从 YAML 加载注册用例"""
    return load_register_data()["test_register"]


def _case_id(case):
    """取用例 ID 作为 pytest parametrize 的显示名（如 TC-LOGIN-001）"""
    return case["id"]


@allure.epic("AI健康管理系统")
@allure.feature("登录注册")
class TestLogin:
    """登录接口测试 — 7 条数据驱动用例（成功/密码错误/不存在/空用户名/空密码/空请求体）"""

    @allure.story("登录")
    @pytest.mark.parametrize("case", _get_login_cases(), ids=_case_id)
    def test_login(self, case):
        """数据驱动登录测试：遍历 YAML 中所有登录场景"""
        api = LoginAPI()
        req = case["request"]
        # 失败场景不走 do_post 的默认 20000 断言，用 _do 手动控制
        data = api._do("POST", req["path"], json=req["json"])

        if case["expected"].get("code") is not None:
            assert data["code"] == case["expected"]["code"]
        if case["expected"].get("code_not") is not None:
            assert data["code"] != case["expected"]["code_not"]
        if case["expected"].get("has_token"):
            assert data["data"]["token"] is not None


@allure.epic("AI健康管理系统")
@allure.feature("登录注册")
class TestRegister:
    """注册接口测试 — 4 条数据驱动用例（成功/重复用户名/缺少用户名/缺少密码）"""

    TEST_USERNAME = "pytest_register_test"

    @classmethod
    def teardown_class(cls):
        """测试类结束后清理注册产生的测试用户"""
        delete_user_by_username(cls.TEST_USERNAME)
        delete_user_by_username("no_pass_user")

    @allure.story("注册")
    @pytest.mark.parametrize("case", _get_register_cases(), ids=_case_id)
    def test_register(self, case):
        """数据驱动注册测试：先清理残留用户，再执行注册并校验结果"""
        api = LoginAPI()
        params = dict(case["params"])
        # 清理可能残留的测试用户，避免"用户名已存在"干扰测试
        cleanup_users = ["pytest_register_test", "no_pass_user"]
        if params.get("username") in cleanup_users:
            delete_user_by_username(params["username"])
            params.setdefault("phone", "")
            params.setdefault("email", "")

        data = api.do_post("/user/register", json=params, expected_code=None)

        if case["expected"].get("code") is not None:
            assert data.get("code") == case["expected"]["code"], f"{case['name']}: {data}"
        if case["expected"].get("code_not") is not None:
            assert data.get("code") != case["expected"]["code_not"], f"{case['name']}: {data}"
        # TC-REG-001 注册成功需额外验证数据库确实写入了
        if case["id"] == "TC-REG-001":
            assert user_exists("pytest_register_test")
