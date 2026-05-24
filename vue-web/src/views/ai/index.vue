<template>
  <div class="background-view">
    <div class="chat-view">
      <div class="chat-panel">
        <div class="message-panel">
          <!-- 消息列表 -->
          <div class="message-list" ref="messageContainer">
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="['message-row', message.type]"
            >
              <div v-if="message.type === 'ai'" class="message-avatar">
                <img :src="aiAvatar" alt="AI Avatar" class="avatar" />
              </div>
              <div class="message-bubble-wrapper">
                <!-- 推理过程折叠面板 -->
                <div v-if="message.reasoning" class="reasoning-box">
                  <div class="reasoning-header" @click="toggleReasoning(index)">
                    <span class="reasoning-icon">{{ message.reasoningOpen ? '▼' : '▶' }}</span>
                    <span>推理过程</span>
                  </div>
                  <div v-show="message.reasoningOpen" class="reasoning-content">
                    {{ message.reasoning }}
                  </div>
                </div>
                <!-- 正文内容 -->
                <div v-if="message.content" :class="['message', message.type === 'user' ? 'user-message' : 'ai-message']">
                  {{ message.content }}
                </div>
              </div>
              <div v-if="message.type === 'user'" class="message-avatar">
                <img :src="userAvatar" alt="User Avatar" class="avatar" />
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="message-input">
            <el-input
              v-model="userInput"
              type="textarea"
              :rows="3"
              placeholder="请输入您的问题..."
              @keyup.enter.native="sendMessage"
            />
            <el-button type="primary" @click="sendMessage" :loading="loading">
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AiAssistant',
  data() {
    return {
      messages: [
        {
          type: 'ai',
          content: '你好！我是您的AI健康助手，请问有什么可以帮您的吗？（输入"AI健康建议" 会根据用户历史健康数据给出建议！）',
          reasoning: '',
          reasoningOpen: true,
          _rawBuffer: ''
        }
      ],
      userInput: '',
      loading: false,
      socket: null,
      userAvatar: require('@/assets/user.jpg'),
      aiAvatar: require('@/assets/ai.jpg'),
      isConnected: false,
      reconnectAttempts: 0,
      maxReconnectAttempts: 5,
      reconnectInterval: 3000,
      username: localStorage.getItem('username')
    }
  },
  mounted() {
    this.setupWebSocket()
  },
  beforeDestroy() {
    this.closeWebSocket()
  },
  methods: {
    setupWebSocket() {
      try {
        if (this.socket) {
          this.socket.close()
          this.socket = null
        }

        const wsUrl = `ws://localhost:8080/ws/chat`
        console.log('正在连接到WebSocket服务器:', wsUrl)
        this.socket = new WebSocket(wsUrl)

        const connectionTimeout = setTimeout(() => {
          if (!this.isConnected) {
            console.error('WebSocket连接超时')
            this.closeWebSocket()
            this.handleReconnect()
          }
        }, 5000)

        this.socket.onopen = (event) => {
          clearTimeout(connectionTimeout)
          console.log('WebSocket连接已建立')
          this.isConnected = true
          this.reconnectAttempts = 0
          this.$message.success('已连接到AI助手服务')
        }

        this.socket.onmessage = (event) => {
          try {
            let chunk = event.data
            if (chunk.startsWith('data:')) {
              chunk = chunk.substring(5)
            }
            if (chunk.includes('[DONE]')) {
              this.loading = false
              return
            }
            if (chunk.includes('[ERROR]')) {
              this.loading = false
              this.$message.error('AI服务出错，请重试')
              return
            }
            const lastMessage = this.messages[this.messages.length - 1]
            if (!lastMessage || lastMessage.type !== 'ai') return

            // 追加到原始缓冲区
            if (!lastMessage._rawBuffer) lastMessage._rawBuffer = ''
            lastMessage._rawBuffer += chunk

            // 解析 <think> 标签
            const raw = lastMessage._rawBuffer
            const thinkStart = raw.indexOf('<think>')
            const thinkEnd = raw.indexOf('</think>')

            if (thinkStart >= 0) {
              if (thinkEnd >= 0) {
                // 完整的 think 块
                lastMessage.reasoning = raw.substring(thinkStart + 7, thinkEnd).trim()
                lastMessage.content = raw.substring(thinkEnd + 8).trim()
              } else {
                // think 已开始但未结束，显示推理中
                lastMessage.reasoning = raw.substring(thinkStart + 7).trim()
                lastMessage.content = ''
              }
            } else {
              // 没有 think 标签，直接当正文
              lastMessage.content = raw.trim()
            }

            this.scrollToBottom()
          } catch (error) {
            console.error('处理WebSocket消息时出错:', error)
          }
        }

        this.socket.onerror = (error) => {
          console.error('WebSocket错误:', error)
          this.isConnected = false
          this.handleReconnect()
        }

        this.socket.onclose = (event) => {
          console.log('WebSocket连接已关闭', event)
          this.isConnected = false
          if (!event.wasClean) {
            this.handleReconnect()
          }
        }
      } catch (error) {
        console.error('WebSocket创建失败:', error)
        this.$message.error(`连接失败: ${error.message}`)
        this.handleReconnect()
      }
    },
    toggleReasoning(index) {
      this.messages[index].reasoningOpen = !this.messages[index].reasoningOpen
      this.$nextTick(() => this.scrollToBottom())
    },
    handleReconnect() {
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        this.$message.error('无法连接到AI助手服务，请稍后再试')
        this.isConnected = false
        return
      }
      this.reconnectAttempts++
      const nextAttemptIn = this.reconnectInterval / 1000
      this.$message.warning(`连接失败，${nextAttemptIn}秒后尝试第${this.reconnectAttempts}次重连...`)
      setTimeout(() => {
        this.setupWebSocket()
      }, this.reconnectInterval)
    },
    closeWebSocket() {
      if (this.socket) {
        this.socket.close()
        this.socket = null
        this.isConnected = false
      }
    },
    async sendMessage() {
      if (!this.userInput.trim()) return

      if (!this.isConnected) {
        this.$message.warning('正在连接到AI助手服务...')
        this.setupWebSocket()
        return
      }

      this.messages.push({
        type: 'user',
        content: this.userInput
      })
      const userMessage = this.userInput
      this.userInput = ''

      // 占位AI消息
      this.messages.push({
        type: 'ai',
        content: '',
        reasoning: '',
        reasoningOpen: true,
        _rawBuffer: ''
      })

      this.loading = true
      this.scrollToBottom()

      try {
        const message = {
          type: 'message',
          text: userMessage,
          username: this.username
        }
        if (this.socket.readyState === WebSocket.OPEN) {
          this.socket.send(JSON.stringify(message))
        } else {
          throw new Error('WebSocket连接未就绪')
        }
      } catch (error) {
        console.error('发送消息失败:', error)
        this.$message.error('发送失败，请重试')
        this.loading = false
        this.messages.pop()
        this.handleReconnect()
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
.background-view {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.chat-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.chat-panel {
  width: 90%;
  max-width: 800px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.message-panel {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message-row {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.message-row.user {
  justify-content: flex-end;
}

.message-row.ai {
  justify-content: flex-start;
}

.message-avatar {
  margin: 0 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.message-bubble-wrapper {
  max-width: 70%;
}

.message {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
}

.user-message {
  background-color: #409EFF;
  color: white;
}

.ai-message {
  background-color: #f4f4f5;
  color: #333;
}

/* 推理过程面板 */
.reasoning-box {
  margin-bottom: 8px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fafafa;
}

.reasoning-header {
  padding: 8px 12px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.reasoning-header:hover {
  background-color: #f0f0f0;
}

.reasoning-icon {
  font-size: 10px;
  width: 14px;
  text-align: center;
  flex-shrink: 0;
}

.reasoning-content {
  padding: 10px 14px;
  font-size: 13px;
  line-height: 1.6;
  color: #888;
  border-top: 1px solid #e8e8e8;
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
}

.message-input {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.message-input .el-textarea {
  flex: 1;
}

.message-input .el-button {
  align-self: flex-end;
}
</style>
