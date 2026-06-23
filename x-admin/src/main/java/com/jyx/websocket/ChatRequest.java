package com.jyx.websocket;

import lombok.Data;

@Data
public class ChatRequest {
    private String type;
    private String text;
    private String msg;
    private String userId;
    private String username;
}
