package com.jyx.websocket;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.jyx.dify.DifyService;
import com.jyx.healthsys.service.IBodyNotesService;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.io.IOException;

@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {
    private final DifyService difyService;
    private final IBodyNotesService bodyNotesService;

    public ChatWebSocketHandler(DifyService difyService, IBodyNotesService bodyNotesService) {
        this.difyService = difyService;
        this.bodyNotesService = bodyNotesService;
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws IOException {
        String payload = message.getPayload();
        ChatRequest request = parseMessage(payload);
        String question = request.getText();
        String username = request.getUsername();

        Flux<String> aiResponse = difyService.chatStream(question, username)
                .map(content -> "data:" + content)
                .concatWith(Mono.just("data:[DONE]"));

        aiResponse.subscribe(response -> {
            try {
                session.sendMessage(new TextMessage(response));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }, error -> {
            error.printStackTrace();
            try {
                session.sendMessage(new TextMessage("data:[ERROR]\n\n"));
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }

    private ChatRequest parseMessage(String payload) {
        ObjectMapper mapper = new ObjectMapper();
        try {
            return mapper.readValue(payload, ChatRequest.class);
        } catch (Exception e) {
            throw new RuntimeException("Invalid message format: " + payload, e);
        }
    }
}
