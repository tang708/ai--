"""YAML 测试数据加载器，支持 ${VAR} 占位符解析

设计动机：测试数据和测试账号分离。
- YAML 文件里用 ${TEST_ADMIN.username} 引用配置中的真实账号
- 避免密码等敏感值硬编码在 data 文件中
"""
import os
import re
import yaml
from base_Tool.my_logger import mylogger


def _resolve_value(value, context):
    """递归解析字符串中的 ${VAR} 占位符，支持嵌套访问如 ${TEST_ADMIN.username}"""
    if isinstance(value, str):
        def replacer(m):
            path = m.group(1).split(".")
            obj = context
            for key in path:
                obj = obj.get(key, {}) if isinstance(obj, dict) else getattr(obj, key, "")
            return str(obj)
        return re.sub(r'\$\{([^}]+)\}', replacer, value)
    elif isinstance(value, dict):
        return {k: _resolve_value(v, context) for k, v in value.items()}
    elif isinstance(value, list):
        return [_resolve_value(v, context) for v in value]
    return value


def my_read_yaml(file_name, context=None):
    """加载 YAML 文件并解析占位符

    Args:
        file_name: YAML 文件绝对路径
        context: 占位符上下文字典，如 {"TEST_ADMIN": {"username": "java1234"}}
    """
    mylogger.info("读取测试数据，数据文件为：{}".format(file_name))
    with open(file_name, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if context:
        data = _resolve_value(data, context)
    return data


# caseData 目录路径
_CASEDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "caseData")


def load_yaml(filename, context=None):
    """加载 caseData 下的 YAML 文件（兼容旧接口）"""
    path = os.path.join(_CASEDATA_DIR, filename)
    return my_read_yaml(path, context)


def load_login_data(context=None):
    """加载登录测试数据"""
    return load_yaml("登录注册数据/login_data.yaml", context)


def load_register_data(context=None):
    """加载注册测试数据"""
    return load_yaml("登录注册数据/register_data.yaml", context)


def load_admin_user_data(context=None):
    """加载管理员用户管理测试数据"""
    return load_yaml("用户管理数据/admin_user_data.yaml", context)


def load_core_flow_data(context=None):
    """加载核心业务流程测试数据"""
    return load_yaml("核心流程数据/core_flow_data.yaml", context)
