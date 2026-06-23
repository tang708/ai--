package com.jyx.dify;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jyx.healthsys.entity.BodyNotes;
import com.jyx.healthsys.service.IBodyNotesService;
import io.netty.channel.ChannelOption;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;
import java.util.*;

@Service
public class DifyService {

    private final WebClient webClient;
    private final IBodyNotesService bodyNotesService;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private static final Logger log = LoggerFactory.getLogger(DifyService.class);

    // username → conversation_id，维持多轮对话
    private final Map<String, String> conversationCache = new HashMap<>();

    public DifyService(
            @Value("${dify.api-url}") String apiUrl,
            @Value("${dify.api-key}") String apiKey,
            IBodyNotesService bodyNotesService) {
        this.bodyNotesService = bodyNotesService;

        // 配置 Netty HttpClient，增大超时时间以适应流式响应
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 30000)
                .responseTimeout(Duration.ofSeconds(120));

        this.webClient = WebClient.builder()
                .baseUrl(apiUrl + "/chat-messages")
                .defaultHeader("Authorization", "Bearer " + apiKey)
                .defaultHeader("Content-Type", "application/json")
                .defaultHeader("User-Agent", "AI-Health-System/1.0")
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .build();
    }

    public Flux<String> chatStream(String userMessage, String username) {
        String conversationId = conversationCache.get(username);

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("query", userMessage);
        body.put("user", username);
        body.put("response_mode", "streaming");
        body.put("conversation_id", conversationId != null ? conversationId : "");

        Map<String, Object> inputs = new LinkedHashMap<>();
        inputs.put("user_message", userMessage);
        inputs.put("username", username);
        inputs.put("health_data", buildHealthDataMap(username));  // 传 Map 而非 JSON 字符串
        body.put("inputs", inputs);

        return webClient.post()
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(body)  // 让 WebClient 自动序列化
                .accept(MediaType.TEXT_EVENT_STREAM)
                .retrieve()
                .bodyToFlux(String.class)
                .doOnNext(raw -> log.info("Dify raw: {}", raw))
                .mapNotNull(chunk -> extractAnswer(chunk, username))
                .doOnError(e -> log.error("Dify error: {}", e.getMessage()));
    }

    /** 解析 Dify SSE 流，提取 answer 增量文本，同时捕获 conversation_id */
    private String extractAnswer(String sseLine, String username) {
        if (sseLine == null || sseLine.isEmpty()) return null;
        // Dify SSE 格式：每行 "data: {...json...}"
        String json = sseLine.startsWith("data:") ? sseLine.substring(5).trim() : sseLine.trim();
        if (json.isEmpty() || "[DONE]".equals(json)) return null;
        try {
            JsonNode node = objectMapper.readTree(json);
            // 只处理 message 事件，跳过 workflow/node 状态事件
            if (!node.has("event") || !"message".equals(node.get("event").asText())) return null;
            // 首次响应保存 conversation_id
            if (node.has("conversation_id") && !node.get("conversation_id").asText().isEmpty()) {
                conversationCache.put(username, node.get("conversation_id").asText());
            }
            if (node.has("answer")) {
                String answer = node.get("answer").asText();
                if (answer.isEmpty()) return null;
                return answer;
            }
        } catch (JsonProcessingException ignored) {
        }
        return null;
    }

    /** 查最新一条健康数据，返回 Map（对应 Dify 的 Object 类型输入） */
    private Map<String, Object> buildHealthDataMap(String username) {
        Map<String, Object> data = new LinkedHashMap<>();
        List<BodyNotes> notes = bodyNotesService.getBodyNotesByUsername(username);
        if (notes != null && !notes.isEmpty()) {
            BodyNotes n = notes.get(0);
            data.put("name", n.getName());
            data.put("age", n.getAge());
            data.put("gender", n.getGender());
            data.put("height", n.getHeight());
            data.put("weight", n.getWeight());
            data.put("bloodSugar", n.getBloodSugar());
            data.put("bloodPressure", n.getBloodPressure());
            data.put("bloodLipid", n.getBloodLipid());
            data.put("heartRate", n.getHeartRate());
            data.put("vision", n.getVision());
            data.put("sleepDuration", n.getSleepDuration());
            data.put("sleepQuality", n.getSleepQuality());
            data.put("smoking", n.isSmoking());
            data.put("drinking", n.isDrinking());
            data.put("exercise", n.isExercise());
            data.put("foodTypes", n.getFoodTypes());
            data.put("waterConsumption", n.getWaterConsumption());
        }
        return data;
    }
}
