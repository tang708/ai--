# AI健康管理系统 — 测试项目

## 项目简介

**AI健康管理系统** 是一个前后端分离架构的健康管理 Web 平台，集成 AI 智能健康助手，支持健康数据管理、运动知识查询、AI 个性化建议等核心功能，采用 JWT + RBAC 五表权限模型。

- **后端**：Spring Boot 3.4.0 + MyBatis-Plus + MySQL 8.0 + Redis + WebSocket
- **前端**：Vue 2.6 + Element UI + Axios + ECharts
- **AI**：DeepSeek V4（Spring AI + WebSocket 流式对话）

## 测试策略

```
              ┌───────────────────────┐
             /       手工探索性测试      \      ← 用例文档驱动，边界条件查漏补缺
            /───────────────────────────\
           /        接口自动化测试         \     ← Python + Requests + Pytest，覆盖 20+ API
          /───────────────────────────────\
         /           单元测试              \    ← 开发侧 JUnit（不在本测试范围）
        └──────────────────────────────────┘
```

本测试项目主要负责 **接口自动化**，辅以手工测试用例文档。

## 工程目录说明

```
tests/
├── README.md                        # 本文件
├── requirements.txt                 # Python 依赖
├── conftest.py                      # Pytest 全局 fixtures（登录态管理）
├── config/
│   ├── __init__.py
│   └── settings.py                  # 环境配置（BASE_URL、DB、测试账号）
├── data/                            # YAML 测试数据文件
│   ├── login_data.yaml              # 登录场景数据
│   ├── register_data.yaml           # 注册场景数据
│   ├── admin_user_data.yaml         # 管理员用户管理数据
│   └── core_flow_data.yaml          # 核心链路数据
├── api_objects/                     # POM 接口对象层
│   ├── __init__.py
│   ├── base_api.py                  # BaseAPI（请求-断言封装）
│   ├── login_api.py                 # 登录注册接口对象
│   ├── user_api.py                  # 用户管理接口对象
│   └── body_api.py                  # 身体信息接口对象
├── utils/
│   ├── __init__.py
│   ├── api_client.py                # Requests Session 封装（自动带 Token）
│   ├── db_helper.py                 # MySQL 辅助（数据一致性校验）
│   └── data_loader.py               # YAML 加载 + ${VAR} 占位符解析
├── api/                             # 接口自动化测试（POM + YAML 数据驱动）
│   ├── __init__.py
│   ├── test_login_register.py       # 登录注册（7+4 parametrize）
│   ├── test_core_flow.py            # 核心业务链路 + 一致性（4 用例）
│   └── test_admin_user_management.py # 管理员 CRUD + 权限（11 用例）
├── test_cases/
│   ├── README.md                    # 用例概览说明
│   ├── api_test_cases.xlsx          # 接口测试用例（83 条，7 模块）
│   └── generate_excel.py            # 用例 Excel 生成脚本
└── reports/                         # Allure 报告输出目录
    └── .gitkeep
```

## 环境准备

### 1. 被测系统启动

**后端**（默认端口 8080）：
```bash
cd x-admin
mvn spring-boot:run
```

### 2. 测试环境

```bash
cd tests
pip install -r requirements.txt
```

- Python 3.8+
- 确保 MySQL 数据库 `db_health` 已初始化（执行 `db_health.sql`）
- 确保 Redis 运行在 localhost:6379

### 3. 环境切换

```bash
# 默认 dev 环境
pytest api/ -v

# 通过环境变量切换
$env:TEST_ENV="prod"; pytest api/ -v
```

## 运行测试

### 全部接口测试

```bash
pytest api/ -v --alluredir=reports/
```

### 按模块运行

```bash
# 登录注册
pytest api/test_login_register.py -v --alluredir=reports/

# 核心业务链路
pytest api/test_core_flow.py -v --alluredir=reports/

# 管理员用户管理
pytest api/test_admin_user_management.py -v --alluredir=reports/
```

## 查看测试报告

```bash
allure serve reports/
```

## 用例概览

详细用例见 [test_cases/api_test_cases.xlsx](test_cases/api_test_cases.xlsx)，共 **83 条**。

| 模块 | 用例数 | P0 | P1 | P2 |
|------|--------|----|----|-----|
| 登录注册 | 17 | 7 | 7 | 3 |
| 权限控制 | 10 | 6 | 3 | 1 |
| 用户管理 | 12 | 6 | 3 | 3 |
| 身体信息管理 | 15 | 7 | 5 | 3 |
| 运动知识查询 | 11 | 4 | 4 | 3 |
| 运动知识管理 | 8 | 3 | 4 | 1 |
| AI对话 | 10 | 3 | 4 | 3 |
| **合计** | **83** | **36** | **30** | **17** |

## 测试报告截图

> 运行 `pytest api/ -v --alluredir=reports/ && allure serve reports/` 后在此处贴截图
