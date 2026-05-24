"""身体信息 API 对象"""
from baseAPI.base_api import BaseAPI


class BodyAPI(BaseAPI):
    """身体信息 + 历史记录接口封装，继承 BaseAPI 的请求-断言能力"""

    def upload(self, body_data):
        """上传身体信息（首次上传）或更新（已有数据时覆盖）"""
        return self.do_post("/user/BodyInformation", json=body_data)

    def get_current(self):
        """获取当前登录用户最新的身体信息"""
        return self.do_get("/user/getBodyInfo")

    def save_history(self, notes_data):
        """保存身体信息历史快照，可保存多个时间点的数据"""
        return self.do_post("/user/BodyInformationNotes", json=notes_data)

    def get_history_list(self, page_no=1, page_size=10):
        """分页获取当前用户的身体信息历史记录"""
        return self.do_get("/user/getUserBodyList",
                           params={"pageNo": page_no, "pageSize": page_size})

    def get_history_by_id(self, notes_id):
        """根据记录 ID 获取单条历史快照详情"""
        return self.do_get(f"/user/getUserBodyById/{notes_id}")

    def delete_history(self, notes_id):
        """根据记录 ID 删除单条历史快照"""
        return self.do_delete(f"/user/deleteUserBodyById/{notes_id}")

    # ── 管理员接口 ──

    def admin_get_body_list(self, page_no=1, page_size=10, name=None):
        """管理员查询所有用户的身体信息（分页）"""
        params = {"pageNo": page_no, "pageSize": page_size}
        if name:
            params["name"] = name
        return self.do_get("/user/getBodyList", params=params)

    def admin_get_body_by_id(self, user_id):
        """管理员根据用户 ID 查询身体信息"""
        return self.do_get(f"/user/getBodyById/{user_id}")

    def admin_update_body(self, body_data):
        """管理员修改用户身体信息"""
        return self.do_put("/user/updateBody", json=body_data)

    def admin_delete_body(self, user_id):
        """管理员删除用户身体信息及关联历史记录"""
        return self.do_delete(f"/user/deleteBodyById/{user_id}")
