# AI 健康管理系统 — Spring Boot 后端

> **GitHub**: https://github.com/tang708/ai-health-admin

AI 健康管理系统的 Java 后端服务，提供 REST API、WebSocket AI 对话、用户认证与健康数据管理。

## 技术栈

- Spring Boot 3.4 + Java 17
- MyBatis-Plus + Spring Data JPA
- MySQL 8.0 + Redis
- Spring AI + Dify 工作流集成
- JWT (jjwt) + RBAC 权限模型
- Spring WebSocket（AI 流式对话）
- SpringDoc OpenAPI（API 文档）

## 快速开始

```bash
# 创建数据库 db_health
# 执行项目根目录的 db_health.sql
mvn spring-boot:run
```

## 环境变量

配置 `DIFY_API_KEY`, `DB_PASSWORD`

## 模块结构

```
src/main/java/com/jyx/
├── config/          # Spring 配置（安全、跨域、OpenAPI）
├── controller/      # REST 控制器（用户、身体数据、运动信息等）
├── entity/          # 数据实体
├── dify/            # Dify 工作流 AI 对话
├── websocket/       # WebSocket AI 流式通信
└── healthsys/       # 健康系统业务逻辑
```
