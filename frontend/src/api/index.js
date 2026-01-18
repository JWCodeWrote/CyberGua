/**
 * API 服务模块
 * 封装后端接口调用
 */
import axios from "axios";

// 创建 axios 实例
const api = axios.create({
  baseURL: "/api",
  timeout: 120000, // 2分钟超时 (AI 生成需要时间)
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * 健康检查
 * @returns {Promise<{status: string, ollama: boolean, timestamp: string}>}
 */
export async function checkHealth() {
  const response = await api.get("/health");
  return response.data;
}

/**
 * 简单版预测 (梅花易数)
 * @param {number[]} nums - 三个数字
 * @param {string} question - 问题
 * @returns {Promise<Object>}
 */
export async function predictSimple(nums, question) {
  const response = await api.post("/predict/simple", {
    nums,
    question,
  });
  return response.data;
}

/**
 * 详细版预测 (命+运+局)
 * @param {Object} params
 * @param {number} params.birthYear - 出生年
 * @param {number} params.birthMonth - 出生月
 * @param {number} params.birthDay - 出生日
 * @param {number} params.birthHour - 出生时 (0-23)
 * @param {string} params.gender - 性别 (male/female)
 * @param {number[]} params.nums - 三个数字
 * @param {string} params.question - 问题
 * @returns {Promise<Object>}
 */
export async function predictDetailed(params) {
  const response = await api.post("/predict/detailed", {
    birth_year: params.birthYear,
    birth_month: params.birthMonth,
    birth_day: params.birthDay,
    birth_hour: params.birthHour,
    gender: params.gender,
    nums: params.nums,
    question: params.question,
  });
  return response.data;
}

/**
 * 追问 AI (基于卦象继续提问)
 * @param {Object} params
 * @param {string} params.question - 追问问题
 * @param {Object} params.hexagram - 当前卦象信息
 * @param {Object} [params.bazi] - 八字信息 (详细版)
 * @param {Object} [params.fengshui] - 风水信息 (详细版)
 * @param {Array} [params.history] - 对话历史
 * @returns {Promise<Object>}
 */
export async function chatFollowup(params) {
  const response = await api.post("/chat", {
    question: params.question,
    hexagram: params.hexagram,
    bazi: params.bazi || null,
    fengshui: params.fengshui || null,
    history: params.history || [],
  });
  return response.data;
}

export default api;
