package com.jyx.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;

import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("AI健康管理系统接口文档")
                        .description("AI健康管理系统 — 前后端分离架构的健康管理平台，"
                                + "支持用户管理、身体信息管理、运动知识查询、"
                                + "病情运动详情、AI智能对话等核心功能。"
                                + "\n\n**认证方式**：先调用 `/user/login` 获取 token，"
                                + "再点击右上角 **Authorize** 按钮，输入 token 值。")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("金义雄")))
                .components(new Components()
                        .addSecuritySchemes("X-Token", new SecurityScheme()
                                .name("X-Token")
                                .type(SecurityScheme.Type.APIKEY)
                                .in(SecurityScheme.In.HEADER)
                                .description("登录后获取的 token，格式：<token值>")))
                .addSecurityItem(new SecurityRequirement().addList("X-Token"));
    }

    @Bean
    public GroupedOpenApi userGroup() {
        return GroupedOpenApi.builder()
                .group("用户管理")
                .pathsToMatch("/user/**")
                .build();
    }

    @Bean
    public GroupedOpenApi roleGroup() {
        return GroupedOpenApi.builder()
                .group("角色管理")
                .pathsToMatch("/role/**")
                .build();
    }

    @Bean
    public GroupedOpenApi menuGroup() {
        return GroupedOpenApi.builder()
                .group("菜单管理")
                .pathsToMatch("/menu/**")
                .build();
    }

    @Bean
    public GroupedOpenApi sportGroup() {
        return GroupedOpenApi.builder()
                .group("运动知识管理")
                .pathsToMatch("/sport/**")
                .build();
    }

    @Bean
    public GroupedOpenApi detailGroup() {
        return GroupedOpenApi.builder()
                .group("病情运动详情")
                .pathsToMatch("/detail/**")
                .build();
    }
}
