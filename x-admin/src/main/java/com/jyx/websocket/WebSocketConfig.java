package com.jyx.websocket;

import com.jyx.dify.DifyService;
import com.jyx.healthsys.service.IBodyNotesService;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import org.springframework.web.socket.server.support.HttpSessionHandshakeInterceptor;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    private final DifyService difyService;
    private final IBodyNotesService bodyNotesService;

    public WebSocketConfig(DifyService difyService, IBodyNotesService bodyNotesService) {
        this.difyService = difyService;
        this.bodyNotesService = bodyNotesService;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new ChatWebSocketHandler(difyService, bodyNotesService), "/ws/chat")
                .setAllowedOrigins("*")
                .addInterceptors(new HttpSessionHandshakeInterceptor());
    }
}
