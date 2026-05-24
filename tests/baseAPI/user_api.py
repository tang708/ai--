"""用户管理 API 对象"""
from baseAPI.base_api import BaseAPI


class UserAPI(BaseAPI):
    """用户 CRUD 接口封装，继承 BaseAPI 的请求-断言能力"""

    def get_list(self, page_no=1, page_size=10, username=None, phone=None):
        """分页获取用户列表，支持按用户名/手机号筛选"""
        params = {"pageNo": page_no, "pageSize": page_size}
        if username:
            params["username"] = username
        if phone:
            params["phone"] = phone
        return self.do_get("/user/list", params=params)

    def get_all(self):
        """获取全部用户列表"""
        return self.do_get("/user/all")

    def get_by_id(self, user_id):
        """根据用户 ID 获取用户详情"""
        return self.do_get(f"/user/{user_id}")

    def add(self, username, password, phone=None, email=None, status="1"):
        """新增用户"""
        return self.do_post("/user/add", json={
            "username": username,
            "password": password,
            "phone": phone or "",
            "email": email or "",
            "status": status,
        })

    def update(self, user_id, username, **kwargs):
        """修改用户信息，支持 keyword 参数扩展"""
        body = {"id": user_id, "username": username}
        body.update(kwargs)
        return self.do_put("/user/update", json=body)

    def delete_user(self, user_id):
        """根据 ID 删除用户（逻辑删除，deleted 置 1）

        命名为 delete_user 而非 delete，避免覆盖 BaseAPI 的方法导致递归调用。
        """
        return self._do("DELETE", f"/user/{user_id}")

    def get_user_id(self):
        """获取当前登录用户的 ID"""
        return self.do_get("/user/getUserId")
