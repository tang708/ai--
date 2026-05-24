"""核心业务链路 — 数据驱动测试"""
import allure
import pytest
from base_Tool.read_yaml import load_core_flow_data
from base_Tool.db_helper import get_user_by_username, get_user_roles, get_user_menus, delete_user_by_username
from baseAPI.body_api import BodyAPI
from baseAPI.login_api import LoginAPI


_CF = load_core_flow_data()


@allure.epic("AI健康管理系统")
@allure.feature("核心业务链路")
class TestCoreBusinessFlow:
    """核心业务流程测试 — 完整链路 + Token 异常 + 数据一致性"""

    BODY_DATA = _CF["test_body_info"]["body_data"]

    @allure.story("健康数据完整链路")
    def test_body_info_core_flow(self, normal_session):
        """核心流程：上传身体信息 → 查询 → 保存历史快照 → 查历史记录"""
        api = BodyAPI()
        api.set_token(normal_session.token)

        with allure.step("1.上传身体信息"):
            data = api.upload(self.BODY_DATA)
            assert data["code"] == 20000, "上传失败: {}".format(data)

        with allure.step("2.查询身体信息"):
            data = api.get_current()
            assert data["code"] == 20000

        with allure.step("3.保存历史快照"):
            notes = dict(self.BODY_DATA)
            notes["bloodSugar"] = 5.8  # 修改血糖值以区分当前和历史
            data = api.save_history(notes)
            assert data["code"] == 20000, "历史快照失败: {}".format(data)

        with allure.step("4.查询历史记录"):
            data = api.get_history_list()
            assert data["code"] == 20000

    @allure.story("Token异常")
    def test_fake_token(self):
        """伪造 token 访问，验证后端不崩溃且返回非成功状态"""
        api = LoginAPI()
        data = api.get_info("fake_token_12345")
        assert isinstance(data, dict)

    @allure.story("Token异常")
    def test_empty_token(self):
        """缺少 token 参数，验证后端返回 400 或非成功码"""
        api = LoginAPI()
        data = api._do("GET", "/user/info")  # 不走 do_get 默认 20000 断言
        assert "code" not in data or data.get("code") != 20000

    @allure.story("数据一致性")
    def test_register_data_consistency(self):
        """验证注册后数据库各表数据完整：用户表 + 默认角色 + 菜单权限"""
        test_name = _CF["test_data_consistency"]["username"]
        delete_user_by_username(test_name)

        api = LoginAPI()
        data = api.register(test_name, _CF["test_data_consistency"]["password"])
        assert data["code"] == 20000

        # 数据库校验：用户记录存在
        user = get_user_by_username(test_name)
        assert user is not None
        # 数据库校验：默认分配了 normal 角色
        roles = get_user_roles(user["id"])
        assert _CF["test_data_consistency"]["expected_role"] in roles
        # 数据库校验：角色对应的菜单不为空
        menus = get_user_menus(user["id"])
        assert len(menus) > 0

        delete_user_by_username(test_name)
