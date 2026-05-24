# AI健康管理系统 — Dify 工作流搭建指南

---

## 一、现状与目标

当前 AI 对话是单轮直调 DeepSeek，system prompt 硬编码在 Java 里，`detail`/`sport_info` 两张表的数据完全没用到。

用 Dify 替换后：Prompt 可视化编辑 + 运动知识库检索 + 对话记忆，**改 Prompt 不用重新部署**。

```
改造前：浏览器 ──WebSocket──> Spring Boot ──Spring AI──> DeepSeek
改造后：浏览器 ──WebSocket──> Spring Boot ──HTTP──> Dify Workflow ──> DeepSeek
                                                         │
                                                         └── 知识库检索（运动健康知识）
```

---

## 二、工作流设计（3 个节点）

```
[开始] → [知识检索：运动知识库] → [LLM：健康助手] → [直接回复]
                                      ↑
                              用户健康数据（API传入）
```

只用一个 LLM 节点处理所有问题。知识检索结果 + 用户健康数据 一起注入 context，LLM 根据问题自行判断侧重点。

---

## 三、搭建步骤

### 步骤 1：部署 Dify

```bash
cd dify/docker
docker compose up -d
# 访问 http://localhost:3000，注册管理员
```

### 步骤 2：创建知识库

**名称**：`运动健康知识库`

将 `detail`（运动疾病映射）和 `sport_info`（运动建议参数）两张表的数据合并为一个文本文件导入。

**上传文件内容如下（已从数据库完整提取）**：

```text
## 跑步
适用疾病：膝盖疼痛
运动方法：选择软质路面，加强膝关节周围肌肉的锻炼
注意事项：注意营养和饮食平衡，避免过度减重或缺氧
建议时长：45分钟
建议心率：140-160次/分
建议频率：4-5次/周
建议速度：10km/h

## 慢跑
适用疾病：哮喘
运动方法：避免在雾霾天气、气温过高或过低的环境下运动，控制呼吸，使用合适的防护装备
注意事项：注意热身，保持呼吸稳定
建议时长：60分钟
建议心率：130-150次/分
建议频率：3-4次/周
建议速度：8km/h

## 快跑
适用疾病：关节炎
运动方法：选择跑步道或软质地面，适当热身
注意事项：避免过度的冲击力，注意饮食，保持合理体重
建议时长：30分钟
建议心率：130-150次/分
建议频率：5-6次/周
建议速度：13km/h

## 长跑
适用疾病：心脏病、高血压、哮喘、慢性阻塞性肺疾病
运动方法：有氧耐力运动，比赛时要跑过规定路程
注意事项：需要注意呼吸和水分补给
建议时长：30分钟-1小时
建议心率：120-160次/分钟
建议频率：3-4次/周
建议速度：10-15千米/小时

## 越野跑
适用疾病：膝盖疼痛
运动方法：选择软质路面，加强膝关节周围肌肉的锻炼
注意事项：注意营养和饮食平衡，避免过度减重或缺氧
建议时长：33分钟
建议心率：130-160次/分
建议频率：3-4次/周
建议速度：8km/h

## 散步
适用疾病：心脏病恢复期、轻度高血压
运动方法：选择平坦路面，保持匀速行走，配合自然呼吸
注意事项：避免饭后立即运动，选择空气质量好的时段
建议时长：30-60分钟
建议心率：90-110次/分
建议频率：每天
建议速度：3-5km/h

## 太极拳
适用疾病：高血压
运动方法：轻柔的动作，缓慢而稳定的呼吸
注意事项：保持心情平稳，不要过度紧张
建议时长：60分钟
建议心率：80-100次/分
建议频率：3-4次/周
建议速度：无

## 瑜伽
适用疾病：脊椎病、膝盖受伤、关节病变
运动方法：选择适合自己身体情况的瑜伽动作，呼吸自然流畅，动作要准确
注意事项：不宜空腹或饱腹时练习，练习后适当休息
建议时长：60分钟
建议心率：90-110次/分
建议频率：1-2次/周
建议速度：无

## 游泳
适用疾病：心脏病、心律失常、哮喘、高血压
运动方法：全身性运动，但患有心脏病等疾病者容易加重病情，应避免。高血压者可适当游泳，但时间和强度不宜过大
注意事项：注意安全避免溺水，保持泳池清洁卫生
建议时长：45分钟
建议心率：120-140次/分
建议频率：3-4次/周
建议速度：2.5km/h

## 体操
适用疾病：心脏病
运动方法：适度运动，不要剧烈运动，保持心情愉快
注意事项：避免在气温过高或过低的环境下运动
建议时长：1-2小时
建议心率：100-120次/分钟
建议频率：3-4次/周
建议速度：无

## 篮球
适用疾病：心脏病、脑血管疾病、骨折
运动方法：保持适度身体活动，掌握正确技巧，遵守比赛规则
注意事项：合理安排训练时间和强度，注意防护措施，保证充足营养
建议时长：120分钟
建议心率：130-150次/分
建议频率：1-2次/周
建议速度：无

## 足球
适用疾病：膝盖疼痛
运动方法：选择软质路面，加强膝关节周围肌肉的锻炼
注意事项：注意营养和饮食平衡，避免过度减重或缺氧
建议时长：90分钟
建议心率：130-150次/分
建议频率：2-3次/周
建议速度：无

## 排球
适用疾病：扭伤
运动方法：注意热身，保持肌肉灵活
注意事项：避免在硬地面和湿滑地面上运动，注意落地姿势
建议时长：1小时
建议心率：100-120次/分钟
建议频率：2-3次/周
建议速度：无

## 网球
适用疾病：肩部受伤、腕关节疼痛、脱臼
运动方法：掌握正确的发球姿势和击球技巧，加强肌肉训练提高关节灵活性
注意事项：选择合适的球拍和鞋子，保持场地干燥，定期身体检查
建议时长：1.5小时
建议心率：100-130次/分钟
建议频率：2-3次/周
建议速度：无

## 羽毛球
适用疾病：肌肉劳损
运动方法：逐渐增加训练量，充足的热身与休息，避免过度用力
注意事项：注意营养和充足睡眠，避免疲劳和缺氧
建议时长：120分钟
建议心率：130-150次/分
建议频率：3-4次/周
建议速度：无

## 橄榄球
适用疾病：骨折
运动方法：选择合适的防护装备，不要使用过度生硬的球
注意事项：规范比赛流程，避免激烈对抗
建议时长：1.5-2小时
建议心率：100-120次/分钟
建议频率：2-3次/周
建议速度：无

## 跆拳道
适用疾病：扭伤、拉伤
运动方法：逐渐增加训练量，充足的热身与休息，避免过度用力
注意事项：注意营养和充足睡眠，避免疲劳和缺氧
建议时长：1小时
建议心率：120-140次/分钟
建议频率：3-4次/周
建议速度：无

## 滑冰
适用疾病：骨折、关节炎、心脏病、高血压
运动方法：穿好防护装备，注意自己的身体状况，避免剧烈运动
注意事项：避免过度运动造成身体损伤
建议时长：1小时
建议心率：100-120次/分钟
建议频率：2-3次/周
建议速度：10-15千米/小时

## 爬山
适用疾病：高血压、心脏病、脑血管疾病
运动方法：选择较平缓的山路，掌握正确的呼吸方法，避免缺氧
注意事项：随时补充水分和能量，注意天气变化，避免恶劣天气攀登
建议时长：60分钟
建议心率：130-150次/分
建议频率：2-3次/周
建议速度：5km/h

## 跳绳
适用疾病：膝盖或脚踝疼痛、肌肉酸痛、运动损伤
运动方法：手持跳绳，双脚交替跳跃
注意事项：需要注意跳绳时的姿势和呼吸
建议时长：30分钟-1小时
建议心率：120-160次/分钟
建议频率：3-4次/周
建议速度：无

## 跳高
适用疾病：扭伤、肌肉拉伤、腰椎间盘突出、关节炎
运动方法：助跑后跳过竞赛高度悬挂的水平杠
注意事项：需要注意跑道、助跑和跳跃姿势
建议时长：1小时
建议心率：120-160次/分钟
建议频率：2-3次/周
建议速度：无

## 跳板
适用疾病：脊椎损伤
运动方法：注意技术细节，逐渐增加训练难度，避免过度用力
注意事项：可选择针对脊柱的力量训练，加强腰背肌群的锻炼
建议时长：1小时
建议心率：120-160次/分钟
建议频率：2-3次/周
建议速度：无

## 跳皮筋
适用疾病：肌肉劳损
运动方法：逐渐增加训练量，充足的热身与休息，避免过度用力
注意事项：注意营养和充足睡眠，避免疲劳和缺氧
建议时长：30分钟-1小时
建议心率：100-120次/分钟
建议频率：3-4次/周
建议速度：无

## 踢毽子
适用疾病：扭伤、拉伤
运动方法：将毽子踢起来并在空中进行一系列动作
注意事项：需要注意毽子的质量和天气情况
建议时长：30分钟-1小时
建议心率：100-120次/分钟
建议频率：3-4次/周
建议速度：无

## 抖空竹
适用疾病：眼疾
运动方法：注意眼睛的休息和保护，不要盯着空竹太久
注意事项：避免在光线昏暗的环境下玩抖空竹
建议时长：30分钟-1小时
建议心率：80-100次/分钟
建议频率：1-2次/周
建议速度：无

## 抽陀螺
适用疾病：高血压
运动方法：避免剧烈运动，不要在悬崖陡坡等高度场所运动
注意事项：避免在气温过高或过低的环境下运动
建议时长：30分钟-1小时
建议心率：80-100次/分钟
建议频率：1-2次/周
建议速度：无

## 拔河
适用疾病：心脏病
运动方法：注意不要过度用力，保持呼吸稳定
注意事项：人数相对平衡，避免人数不足或过多
建议时长：30分钟-1小时
建议心率：100-120次/分钟
建议频率：2-3次/周
建议速度：无

## 放风筝
适用疾病：过敏性鼻炎
运动方法：避免在花粉高发季节和污染严重的地区放风筝
注意事项：选择空气清新的场地，不要在风力过大的环境下放风筝
建议时长：1-2小时
建议心率：80-100次/分钟
建议频率：1-2次/周
建议速度：无

## 扔沙袋
适用疾病：关节疼痛、肌肉拉伤
运动方法：使用适当重量的沙袋，注意热身
注意事项：根据自身情况选择沙袋重量，避免过度用力
建议时长：30分钟-1小时
建议心率：100-120次/分钟
建议频率：2-3次/周
建议速度：无
```

**Dify 知识库设置**：

| 参数 | 值 |
|------|-----|
| 分段标识符 | `##` |
| 分段最大长度 | 500 tokens |
| 检索方式 | 混合检索 |
| Top K | 3 |
| 分数阈值 | 0.5 |

### 步骤 3：创建 Chatflow

Dify 工作室 → 创建应用 → 类型选 **Chatflow** → 名称 `AI健康助手`

添加以下 3 个节点并连接：

#### 节点 1：开始（Start）

定义输入变量：

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `user_message` | String | 用户问题 |
| `username` | String | 用户名 |
| `health_data` | Object | 用户最新健康数据 JSON |

> `health_data` 由后端查 `j_body_notes` 拼好传入，结构见步骤 4。

#### 节点 2：知识检索

- 选择知识库「运动健康知识库」
- 查询内容：`{{#Start.user_message#}}`
- 输出变量：`knowledge_context`

#### 节点 3：LLM

- 模型：DeepSeek-V3（或 DeepSeek-R1）
- 上下文：开启
- 记忆：最近 10 轮

**SYSTEM Prompt**：

```
你是AI健康助手，专业的健康管理顾问。

## 约束
不做医学诊断，涉及疾病建议就医。
禁止使用星号、菱形、箭头等特殊符号，禁止Markdown格式。
回复300字以内，用编号分段，直接给结论不做多余铺垫。

## 运动知识库（仅供参考，如果与问题无关则忽略）
{{#知识检索.knowledge_context#}}

## 用户健康数据（如果为空则说明用户未上传）
{{#Start.health_data#}}

## 回答框架
1. 如果是健康评估类问题：指出最需关注的1-2个指标，给运动建议、饮食建议、生活建议。
2. 如果是运动知识类问题：基于知识库回答，明确适用疾病、建议时长频率、注意事项。
3. 如果是打招呼或闲聊：简短友好回应，引导到健康话题。
```

**USER Prompt**：`{{#Start.user_message#}}`

---

### 步骤 4：后端改造

#### 4.1 新增依赖（pom.xml）

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

#### 4.2 新增配置（application.yml）

```yaml
dify:
  api-url: http://localhost:5001
  api-key: app-xxxxxxxx  # Dify 后台发布后获取
```

#### 4.3 新增 DifyService.java

`x-admin/src/main/java/com/jyx/dify/DifyService.java`：

```java
package com.jyx.dify;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jyx.healthsys.entity.BodyNotes;
import com.jyx.healthsys.service.IBodyNotesService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.*;

@Service
public class DifyService {

    private final WebClient webClient;
    private final IBodyNotesService bodyNotesService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    // conversation_id 缓存：username → conversationId
    private final Map<String, String> conversationCache = new HashMap<>();

    public DifyService(
            @Value("${dify.api-url}") String apiUrl,
            @Value("${dify.api-key}") String apiKey,
            IBodyNotesService bodyNotesService) {
        this.bodyNotesService = bodyNotesService;
        this.webClient = WebClient.builder()
                .baseUrl(apiUrl + "/v1/chat-messages")
                .defaultHeader("Authorization", "Bearer " + apiKey)
                .defaultHeader("Content-Type", "application/json")
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
        inputs.put("health_data", buildHealthData(username));
        body.put("inputs", inputs);

        try {
            return webClient.post()
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(objectMapper.writeValueAsString(body))
                    .accept(MediaType.TEXT_EVENT_STREAM)
                    .retrieve()
                    .bodyToFlux(String.class)
                    .mapNotNull(chunk -> extractAnswer(chunk, username));
        } catch (JsonProcessingException e) {
            return Flux.error(e);
        }
    }

    /** 解析 Dify SSE 流，提取 answer 文本，同时捕获 conversation_id */
    private String extractAnswer(String sseLine, String username) {
        if (sseLine == null || !sseLine.startsWith("data:")) return null;
        String json = sseLine.substring(5).trim();
        if (json.isEmpty() || "[DONE]".equals(json)) return null;
        try {
            JsonNode node = objectMapper.readTree(json);
            // 首次响应时保存 conversation_id
            if (node.has("conversation_id")) {
                conversationCache.put(username, node.get("conversation_id").asText());
            }
            // 提取 answer 增量
            if (node.has("answer")) {
                return node.get("answer").asText();
            }
        } catch (JsonProcessingException ignored) {
        }
        return null;
    }

    private Map<String, Object> buildHealthData(String username) {
        Map<String, Object> data = new LinkedHashMap<>();
        List<BodyNotes> notes = bodyNotesService.getBodyNotesByUsername(username);
        if (notes == null || notes.isEmpty()) return data;
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
        return data;
    }
}
```

#### 4.4 修改 WebSocket Handler

修改 `ChatWebSocketHandler.java`：注入 `DifyService`，替换原来的 `wsOpenAiChatModel` 调用。

```java
// 构造器新增 DifyService 参数
public ChatWebSocketHandler(DifyService difyService, IBodyNotesService bodyNotesService) {
    this.difyService = difyService;
    this.bodyNotesService = bodyNotesService;
}

// handleTextMessage 中替换：
Flux<String> aiResponse = difyService.chatStream(question, username)
        .map(content -> "data:" + content + "\n\n")
        .concatWith(Mono.just("data:[DONE]\n\n"));
```

同时修改 `WebSocketConfig.java` 的构造器对应传参。

#### 4.5 不再需要的文件

改造后可以删除：
- `wsOpenAiChatModel.java`（功能被 DifyService 替代）
- `application.yml` 中 `spring.ai.openai` 相关配置

---

### 步骤 5：发布与测试

1. Dify 工作室点击「发布」
2. 应用 → 访问 API → 生成 API 密钥 → 填入 `application.yml` 的 `dify.api-key`
3. 启动后端，打开前端 AI 助手页面测试

**验证用例**：

| 输入 | 预期 |
|------|------|
| "我膝盖疼适合什么运动" | 命中知识库，返回具体运动建议 |
| "AI健康建议" | 结合用户健康数据给出评估 |
| "太极拳适合高血压吗" | 命中太极拳条目，回答适用疾病和注意事项 |
| "你好" | 简短友好回应 |

---

## 四、改造对比

| 维度 | 改造前 | 改造后 |
|------|--------|--------|
| Prompt 管理 | Java 代码硬编码 | Dify 可视化，改完即生效 |
| 运动知识库 | `detail`/`sport_info` 表闲置 | 知识库检索驱动 |
| 对话记忆 | 无 | 10 轮上下文窗口 |
| 模型切换 | 改 yml 重启 | Dify 后台一键切换 |
| 可观测性 | 无 | 日志、Token 用量、成本统计 |
| 节点数 | — | 3 个（开始 → 检索 → LLM） |
