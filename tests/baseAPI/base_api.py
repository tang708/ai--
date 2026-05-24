"""API 基类：封装 requests.Session + Token 管理 + 请求-断言模式

合并了原 utils/api_client.py 和 api_objects/base_api.py 的功能：
- Session 自动维护 Cookie
- X-Token 请求头自动注入
- do_get/do_post 等方法默认断言 code==20000
"""
import requests
from config import BASE_URL
from base_Tool.my_logger import mylogger


class BaseAPI:
    """所有 API 对象基类，提供统一的 HTTP 请求和业务码校验"""

    def __init__(self):
        """初始化 Session 和 Token"""
        self.session = requests.Session()
        self.token = None

    def set_token(self, token):
        """设置认证 Token，后续所有请求自动携带 X-Token 请求头"""
        self.token = token
        self.session.headers["X-Token"] = token

    def _url(self, path):
        """拼接完整请求 URL"""
        return f"{BASE_URL}{path}"

    def _log(self, method, url, resp):
        """记录请求日志：方法、URL、状态码、响应体"""
        mylogger.info("[{}] {} → {}".format(method, url, resp.status_code))
        try:
            mylogger.info("  Response: {}".format(resp.json()))
        except Exception:
            mylogger.info("  Response: {}".format(resp.text[:200]))

    def my_request(self, method, url, **kwargs):
        """通用 HTTP 请求，自动拼接 BASE_URL，失败时抛出异常"""
        full_url = self._url(url) if not url.startswith("http") else url
        mylogger.info("开始请求接口：{}，请求方式：{}，请求参数：{}".format(full_url, method, kwargs))
        try:
            resp = requests.request(method=method, url=full_url, **kwargs)
            self._log(method, full_url, resp)
            return resp
        except Exception:
            mylogger.warning("接口请求失败，请检查请求信息！！")
            raise

    # ── 便捷方法（带业务码断言） ──

    def _do(self, method, path, expected_code=None, **kwargs):
        """执行请求并校验业务状态码

        expected_code=None 时不校验，适用于失败场景（如登录密码错误期望 code!=20000）
        """
        resp = self.my_request(method, path, **kwargs)
        data = resp.json() if resp.text else {}
        if expected_code is not None:
            assert data.get("code") == expected_code, f"{method} {path} → {data}"
        return data

    def do_get(self, path, expected_code=20000, **kwargs):
        """发起 GET 请求，默认断言 code==20000"""
        return self._do("GET", path, expected_code, **kwargs)

    def do_post(self, path, expected_code=20000, **kwargs):
        """发起 POST 请求，默认断言 code==20000"""
        return self._do("POST", path, expected_code, **kwargs)

    def do_put(self, path, expected_code=20000, **kwargs):
        """发起 PUT 请求，默认断言 code==20000"""
        return self._do("PUT", path, expected_code, **kwargs)

    def do_delete(self, path, expected_code=20000, **kwargs):
        """发起 DELETE 请求，默认断言 code==20000"""
        return self._do("DELETE", path, expected_code, **kwargs)
