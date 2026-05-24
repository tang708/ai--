"""全局环境配置，通过 TEST_ENV 环境变量切换多环境

使用方式：
  $env:TEST_ENV="prod"; pytest case/ -v     # Windows PowerShell
  TEST_ENV=prod pytest case/ -v              # Linux/Mac

导出变量：
  BASE_URL / FRONTEND_URL — 被测系统地址
  DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME — 数据库连接
  TEST_ADMIN / TEST_NORMAL — 预置测试账号
"""
import os
from dotenv import load_dotenv
load_dotenv('F:/jinAI/.env')

ENV = os.getenv("TEST_ENV", "dev")

_config = {
    "dev": {
        "BASE_URL": "http://localhost:8080",
        "FRONTEND_URL": "http://localhost:9528",
        "DB_HOST": "localhost",
        "DB_PORT": 3306,
        "DB_USER": "root",
        "DB_PASSWORD": os.getenv("DB_PASSWORD", "123456"),
        "DB_NAME": "db_health",
    },
    "prod": {
        "BASE_URL": "http://localhost:8080",
        "FRONTEND_URL": "http://localhost:9528",
        "DB_HOST": "localhost",
        "DB_PORT": 3306,
        "DB_USER": "root",
        "DB_PASSWORD": os.getenv("DB_PASSWORD", "123456"),
        "DB_NAME": "db_health",
    },
}

_current = _config[ENV]

BASE_URL = _current["BASE_URL"]
FRONTEND_URL = _current["FRONTEND_URL"]
DB_HOST = _current["DB_HOST"]
DB_PORT = _current["DB_PORT"]
DB_USER = _current["DB_USER"]
DB_PASSWORD = _current["DB_PASSWORD"]
DB_NAME = _current["DB_NAME"]

# 预置测试账号 — 被测系统初始化脚本(db_health.sql)中已创建
TEST_ADMIN = {"username": "java1234", "password": "123456"}
TEST_NORMAL = {"username": "Alice", "password": "123456"}
