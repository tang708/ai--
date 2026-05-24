# AI 健康管理系统

> **GitHub**: https://github.com/tang708/ai--

基于 Spring Boot + Vue.js 的前后端分离健康管理系统，集成 AI 智能健康助手，支持用户健康数据管理与运动知识咨询。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Spring Boot 3.4 + MyBatis-Plus + Spring AI + JPA |
| 前端 | Vue 2 + Element UI + Vuex + WebSocket |
| 数据库 | MySQL 8.0 + Redis |
| AI | Dify Workflow + DeepSeek / OpenAI |
| 认证 | JWT + RBAC 权限模型 |
| 文档 | SpringDoc OpenAPI |

## 功能

- **用户管理**: 注册/登录（JWT）、RBAC 权限（管理员/普通用户）
- **健康数据**: 身体信息录入、运动记录、健康指标追踪
- **AI 健康助手**: WebSocket 流式对话，结合用户健康数据给出个性化建议
- **运动知识库**: 结构化运动知识查询
- **Dify 工作流**: AI 对话接口（替代直接调用模型）

## 项目结构

```
├── x-admin/                # Spring Boot 后端
│   └── src/main/java/com/jyx/
│       ├── controller/     # REST API
│       ├── dify/           # Dify 工作流集成
│       └── config/         # 安全/WebSocket 配置
├── vue-web/                # Vue 2 前端
│   └── src/
│       ├── views/          # 页面（登录、健康数据、AI 对话）
│       ├── store/          # Vuex 状态管理
│       └── utils/          # 请求封装、Token 管理
├── dify工作流/             # Dify 工作流配置与测试
├── tests/                  # pytest 自动化测试套件
└── db_health.sql           # 数据库初始化
```

## 快速开始

### 后端
```bash
cd x-admin
# 创建数据库 db_health，执行 db_health.sql
# Spring Boot 配置见 application.yml
mvn spring-boot:run
```

### 前端
```bash
cd vue-web
npm install && npm run dev
```

### 测试
```bash
cd tests
pip install -r requirements.txt
pytest case/ -v
```

## 环境变量

配置 `DIFY_API_KEY`, `DB_PASSWORD`
