/**
 * 时空指挥中心 - 前端控制器
 * Features: SSE 连接, Agent 状态可视化, 打字机效果, 聊天记录持久化
 */

// ===== 配置 =====
const API_BASE_URL = 'http://127.0.0.1:8000';

// ===== DOM 元素 =====
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const taskLog = document.getElementById('taskLog');

// ===== Agent 管理 =====
const agents = {
    concierge: document.getElementById('agent-concierge'),
    scout: document.getElementById('agent-scout'),
    meteorologist: document.getElementById('agent-meteorologist')
};

// ===== 状态管理 =====
let chatHistory = [];

// ===== 初始化 =====
function init() {
    loadHistory();
    addLog('时空指挥中心已启动');
    console.log('🚀 HelloAgents 时空指挥中心 v1.1');
}

// ===== 持久化工具 =====
function saveHistory() {
    localStorage.setItem('chat_history', JSON.stringify(chatHistory));
}

function loadHistory() {
    const saved = localStorage.getItem('chat_history');
    if (saved) {
        try {
            chatHistory = JSON.parse(saved);
            // 渲染历史消息
            chatHistory.forEach(msg => {
                renderMessage(msg.content, msg.type);
            });
            // 滚动到底部
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // 如果有历史消息，移除欢迎页
            if (chatHistory.length > 0) {
                const welcome = chatMessages.querySelector('.welcome-box');
                if (welcome) welcome.remove();
            }
        } catch (e) {
            console.error('加载历史记录失败:', e);
            chatHistory = [];
        }
    }
}

// 仅渲染 DOM，不修改数据
// 仅渲染 DOM，不修改数据
function renderMessage(content, type) {
    // 确定角色和头像
    let role = 'agent';
    let avatarSrc = 'assets/doraemon.png'; // 默认：哆啦A梦

    if (type === 'user') {
        role = 'user';
        avatarSrc = 'assets/nobita.png'; // 用户：大雄
    } else if (type === 'tool-call') {
        // 工具调用通常不显示独立头像，或者保留 agent 头像
    } else if (type === 'thinking') {
        // 思考过程也归属 agent
    }

    // 创建容器
    const row = document.createElement('div');
    row.className = `message-row ${role} ${type}`;

    // 创建头像
    const avatar = document.createElement('img');
    avatar.src = avatarSrc;
    avatar.className = 'message-avatar';
    avatar.alt = role;

    // 创建气泡
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = content;

    // 组装
    row.appendChild(avatar);
    row.appendChild(bubble);

    chatMessages.appendChild(row);
    return bubble; // 返回气泡元素以便 updateLastMessage 更新文本
}

// 添加新消息 (更新数据 + 渲染)
function addMessage(content, type = 'agent') {
    // 移除欢迎消息
    const welcome = chatMessages.querySelector('.welcome-box');
    if (welcome) welcome.remove();

    // 保存到历史
    chatHistory.push({ type, content });
    saveHistory();

    // 渲染
    const bubble = renderMessage(content, type);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return bubble;
}

// 更新最后一条消息的内容 (流式输出用)
function updateLastMessage(content) {
    if (chatHistory.length === 0) return;

    // 更新数据
    const lastMsg = chatHistory[chatHistory.length - 1];
    lastMsg.content = content;
    saveHistory();

    // 更新 DOM
    const lastRow = chatMessages.lastElementChild;
    // 确保找到的是 message-bubble
    if (lastRow) {
        const bubble = lastRow.querySelector('.message-bubble') || lastRow;
        if (bubble) {
            bubble.textContent = content;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}

function addLog(text) {
    const li = document.createElement('li');
    li.className = 'log-item';
    li.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
    taskLog.insertBefore(li, taskLog.firstChild);
}

function setAgentStatus(agentId, status, statusText) {
    const card = agents[agentId];
    if (!card) return;

    const dot = card.querySelector('.status-dot');
    const text = card.querySelector('.status-text');

    // 重置所有状态
    dot.className = 'status-dot';
    card.classList.remove('active');

    // 设置新状态
    if (status === 'working') {
        dot.classList.add('working');
        card.classList.add('active');
    } else if (status === 'success') {
        dot.classList.add('success');
    } else if (status === 'error') {
        dot.classList.add('error');
    } else {
        dot.classList.add('idle');
    }

    text.textContent = statusText || status;
}

function setLoading(loading) {
    sendBtn.disabled = loading;
    sendBtn.classList.toggle('loading', loading);
    userInput.disabled = loading;
}

// ===== SSE 流式处理 =====
async function sendMessage(message) {
    if (!message.trim()) return;

    // 显示用户消息
    addMessage(message, 'user');
    addLog(`用户: ${message.slice(0, 30)}...`);

    // 清空输入
    userInput.value = '';
    setLoading(true);

    // 激活 Concierge
    setAgentStatus('concierge', 'working', '分析中...');

    try {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error('API 请求失败');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        // 状态追踪
        let currentType = null; // 当前正在接收的消息类型

        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // 保留不完整的行

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;

                const data = line.slice(6); // 去掉 "data: "

                if (data === '[DONE]') {
                    setAgentStatus('concierge', 'success', '完成');
                    addLog('任务完成');
                    continue;
                }

                // 解析事件类型 (简化版: 通过关键词判断)
                if (data.includes('思考') || data.includes('Thinking')) {
                    // 如果当前不是 thinking 状态，开始新消息
                    if (currentType !== 'thinking') {
                        addMessage('', 'thinking');
                        currentType = 'thinking';
                    }
                    // 追加内容
                    const lastMsg = chatHistory[chatHistory.length - 1];
                    updateLastMessage(lastMsg.content + data);
                    addLog('正在思考...');
                }
                else if (data.includes('工具') || data.includes('Tool')) {
                    // 工具调用通常是离散消息
                    if (data.includes('get_weather') || data.includes('天气')) {
                        setAgentStatus('meteorologist', 'working', '查询天气...');
                        addLog('调用气象员');
                    } else if (data.includes('search_poi') || data.includes('搜索')) {
                        setAgentStatus('scout', 'working', '搜索中...');
                        addLog('调用侦察兵');
                    }

                    addMessage(data, 'tool-call');
                    currentType = 'tool-call';
                }
                else if (data.includes('执行完成') || data.includes('Result')) {
                    // 工具执行完成 - 通常不需要在界面显示大段结果，这里简化处理
                    setAgentStatus('scout', 'success', '完成');
                    setAgentStatus('meteorologist', 'success', '完成');
                    addLog('工具执行完成');
                }
                else if (data.includes('组织') || data.includes('最终')) {
                    if (currentType !== 'agent') {
                        addMessage('', 'agent');
                        currentType = 'agent';
                    }
                    setAgentStatus('concierge', 'working', '整理回复...');
                }
                else {
                    // 普通文本 (打字机效果)
                    if (currentType !== 'agent') {
                        addMessage('', 'agent');
                        currentType = 'agent';
                    }
                    // 追加内容
                    const lastMsg = chatHistory[chatHistory.length - 1];
                    updateLastMessage(lastMsg.content + data);
                }
            }
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage(`❌ 连接失败: ${error.message}`, 'thinking');
        addLog(`错误: ${error.message}`);
        setAgentStatus('concierge', 'error', '错误');
    } finally {
        setLoading(false);
        // 重置所有 Agent 为待命
        setTimeout(() => {
            Object.keys(agents).forEach(id => setAgentStatus(id, 'idle', '待命'));
        }, 3000);
    }
}

// ===== 事件绑定 =====
sendBtn.addEventListener('click', () => sendMessage(userInput.value));

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(userInput.value);
    }
});

// ===== 模式切换 =====
const chatModeBtn = document.getElementById('chatModeBtn');
const planModeBtn = document.getElementById('planModeBtn');
const planForm = document.getElementById('planForm');
const agentPanelHeader = document.getElementById('agentPanelHeader');
const generateBtn = document.getElementById('generateBtn');
const destinationInput = document.getElementById('destinationInput');
const daysSelect = document.getElementById('daysSelect');
const itineraryResult = document.getElementById('itineraryResult');

// 模式切换事件
if (chatModeBtn && planModeBtn) {
    chatModeBtn.addEventListener('click', () => {
        chatModeBtn.classList.add('active');
        planModeBtn.classList.remove('active');
        planForm.classList.add('hidden');
        agentPanelHeader.style.display = 'block';
        // 显示agent cards
        document.querySelectorAll('.agent-card').forEach(card => card.style.display = 'flex');
    });

    planModeBtn.addEventListener('click', () => {
        planModeBtn.classList.add('active');
        chatModeBtn.classList.remove('active');
        planForm.classList.remove('hidden');
        agentPanelHeader.style.display = 'none';
        // 隐藏agent cards
        document.querySelectorAll('.agent-card').forEach(card => card.style.display = 'none');
    });
}

// ===== 行程生成 =====
if (generateBtn) {
    generateBtn.addEventListener('click', async () => {
        const destination = destinationInput.value.trim();
        const days = parseInt(daysSelect.value);
        const preferences = [...document.querySelectorAll('.tags-container input:checked')]
            .map(c => c.value);

        if (!destination) {
            alert('请输入目的地！');
            return;
        }

        // 禁用按钮
        generateBtn.disabled = true;
        generateBtn.textContent = '⏳ 生成中...';
        itineraryResult.classList.add('hidden');

        try {
            const response = await fetch(`${API_BASE_URL}/api/itinerary`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ destination, days, preferences })
            });

            if (!response.ok) throw new Error('API 请求失败');

            const data = await response.json();
            displayItinerary(data);

        } catch (error) {
            console.error('Error:', error);
            alert(`生成失败: ${error.message}`);
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = '🚀 生成行程';
        }
    });
}

// ===== 展示行程结果 =====
function displayItinerary(data) {
    itineraryResult.classList.remove('hidden');

    let html = '';

    // 概述
    if (data.summary) {
        html += `<div class="itinerary-summary">${data.summary}</div>`;
    }

    // 每日行程卡片
    for (const day of data.itinerary || []) {
        html += `
            <div class="day-card">
                <h4>📅 第${day.day}天 ${day.date || ''}</h4>
                <div class="weather-tip">🌤️ ${day.weather_tip || day.weather}</div>
                
                <div class="activity-section">
                    <strong>🌅 上午:</strong>
                    <span class="activity-list">${day.morning?.map(p => p.name).join('、') || '自由活动'}</span>
                </div>
                
                <div class="activity-section">
                    <strong>🌇 下午:</strong>
                    <span class="activity-list">${day.afternoon?.map(p => p.name).join('、') || '自由活动'}</span>
                </div>
                
                ${day.dinner ? `
                <div class="activity-section">
                    <strong>🍽️ 晚餐:</strong>
                    <span class="activity-list">${day.dinner.name}</span>
                </div>` : ''}
                
                ${day.hotel ? `
                <div class="activity-section">
                    <strong>🏨 住宿:</strong>
                    <span class="activity-list">${day.hotel.name}</span>
                </div>` : ''}
            </div>
        `;
    }

    // 旅行贴士
    if (data.tips && data.tips.length > 0) {
        html += `
            <div class="tips-section">
                <h4>📌 旅行贴士</h4>
                <ul>
                    ${data.tips.map(t => `<li>${t}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    itineraryResult.innerHTML = html;
}

// 启动
window.onload = init;

