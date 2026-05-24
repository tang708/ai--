"""登录注册 API 对象"""
from baseAPI.base_api import BaseAPI


class LoginAPI(BaseAPI):
    """登录 + 注册接口封装，继承 BaseAPI 的请求-断言能力"""

    def login(self, username, password):
        """用户登录，返回 data 中包含 token"""
        return self.do_post("/user/login", json={
            "username": username, "password": password})

    def register(self, username, password, phone=None, email=None):
        """用户注册，phone/email 未传时填空串"""
        return self.do_post("/user/register", json={
            "username": username,
            "password": password,
            "phone": phone or "",
            "email": email or "",
        })

    def logout(self):
        """用户登出，需 X-Token 请求头"""
        return self.do_post("/user/logout")

    def get_info(self, token):
        """通过 URL 参数获取用户信息（非标准，推荐用 X-Token 方式）"""
        return self.do_get("/user/info", params={"token": token})

    def change_password(self, old_pwd, new_pwd):
        """修改密码"""
        return self.do_put("/user/changePassword", json={
            "oldPassword": old_pwd, "newPassword": new_pwd})
