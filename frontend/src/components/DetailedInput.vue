<script setup>
/**
 * 详细版输入组件
 * 输入八字信息 + 三个数字 + 问题
 */
import { ref, computed } from "vue";
import { predictDetailed } from "../api";

const emit = defineEmits(["submit", "loading", "back"]);

// 八字信息
const birthYear = ref(1990);
const birthMonth = ref(1);
const birthDay = ref(1);
const birthHour = ref(12);
const gender = ref("male");

// 占卜信息
const num1 = ref(null);
const num2 = ref(null);
const num3 = ref(null);
const question = ref("");

const error = ref("");

// 生成年份选项 (1940-2020)
const years = computed(() => {
  const result = [];
  for (let y = 2020; y >= 1940; y--) {
    result.push(y);
  }
  return result;
});

// 时辰选项
const hours = [
  { value: 0, label: "子时 (23:00-01:00)" },
  { value: 2, label: "丑时 (01:00-03:00)" },
  { value: 4, label: "寅时 (03:00-05:00)" },
  { value: 6, label: "卯时 (05:00-07:00)" },
  { value: 8, label: "辰时 (07:00-09:00)" },
  { value: 10, label: "巳时 (09:00-11:00)" },
  { value: 12, label: "午时 (11:00-13:00)" },
  { value: 14, label: "未时 (13:00-15:00)" },
  { value: 16, label: "申时 (15:00-17:00)" },
  { value: 18, label: "酉时 (17:00-19:00)" },
  { value: 20, label: "戌时 (19:00-21:00)" },
  { value: 22, label: "亥时 (21:00-23:00)" },
];

async function submit() {
  // 验证
  if (!num1.value || !num2.value || !num3.value) {
    error.value = "请输入三个数字";
    return;
  }
  if (!question.value.trim()) {
    error.value = "请输入您的问题";
    return;
  }

  error.value = "";
  emit("loading");

  try {
    const result = await predictDetailed({
      birthYear: parseInt(birthYear.value),
      birthMonth: parseInt(birthMonth.value),
      birthDay: parseInt(birthDay.value),
      birthHour: parseInt(birthHour.value),
      gender: gender.value,
      nums: [parseInt(num1.value), parseInt(num2.value), parseInt(num3.value)],
      question: question.value,
    });
    emit("submit", result);
  } catch (e) {
    error.value = e.response?.data?.detail || "请求失败，请确保后端服务已启动";
    emit("submit", { error: error.value, success: false });
  }
}
</script>

<template>
  <div class="fade-in-up max-w-2xl mx-auto">
    <!-- 标题 -->
    <div class="text-center mb-8">
      <h2 class="text-3xl font-bold text-gold mb-2">命运推演</h2>
      <p class="text-base-content/60">综合八字、卦象、风水的完整分析</p>
    </div>

    <!-- 八字信息 -->
    <div class="gua-card rounded-2xl p-6 mb-6">
      <label class="block text-sm font-medium text-secondary mb-4"
        >📜 八字信息 (阳历)</label
      >

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <!-- 年 -->
        <div class="form-control">
          <label class="label"><span class="label-text">年</span></label>
          <select v-model="birthYear" class="select select-bordered select-sm">
            <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
        <!-- 月 -->
        <div class="form-control">
          <label class="label"><span class="label-text">月</span></label>
          <select v-model="birthMonth" class="select select-bordered select-sm">
            <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
          </select>
        </div>
        <!-- 日 -->
        <div class="form-control">
          <label class="label"><span class="label-text">日</span></label>
          <select v-model="birthDay" class="select select-bordered select-sm">
            <option v-for="d in 31" :key="d" :value="d">{{ d }}日</option>
          </select>
        </div>
        <!-- 时辰 -->
        <div class="form-control">
          <label class="label"><span class="label-text">时辰</span></label>
          <select v-model="birthHour" class="select select-bordered select-sm">
            <option v-for="h in hours" :key="h.value" :value="h.value">
              {{ h.label }}
            </option>
          </select>
        </div>
      </div>

      <!-- 性别 -->
      <div class="form-control">
        <label class="label"><span class="label-text">性别</span></label>
        <div class="flex gap-4">
          <label class="label cursor-pointer gap-2">
            <input
              type="radio"
              v-model="gender"
              value="male"
              class="radio radio-primary radio-sm"
            />
            <span class="label-text">男</span>
          </label>
          <label class="label cursor-pointer gap-2">
            <input
              type="radio"
              v-model="gender"
              value="female"
              class="radio radio-secondary radio-sm"
            />
            <span class="label-text">女</span>
          </label>
        </div>
      </div>
    </div>

    <!-- 数字输入 -->
    <div class="gua-card rounded-2xl p-6 mb-6">
      <label class="block text-sm font-medium text-primary mb-4"
        >☯ 报数 (1-64)</label
      >

      <div class="grid grid-cols-3 gap-4">
        <div class="form-control">
          <label class="label"
            ><span class="label-text text-base-content/50">下卦</span></label
          >
          <input
            type="number"
            v-model="num1"
            min="1"
            max="64"
            placeholder="1-64"
            class="input input-bordered input-primary text-center text-xl"
          />
        </div>
        <div class="form-control">
          <label class="label"
            ><span class="label-text text-base-content/50">上卦</span></label
          >
          <input
            type="number"
            v-model="num2"
            min="1"
            max="64"
            placeholder="1-64"
            class="input input-bordered input-primary text-center text-xl"
          />
        </div>
        <div class="form-control">
          <label class="label"
            ><span class="label-text text-base-content/50">动爻</span></label
          >
          <input
            type="number"
            v-model="num3"
            min="1"
            max="64"
            placeholder="1-64"
            class="input input-bordered input-primary text-center text-xl"
          />
        </div>
      </div>
    </div>

    <!-- 问题输入 -->
    <div class="gua-card rounded-2xl p-6 mb-6">
      <label class="block text-sm font-medium text-primary mb-4">☯ 问题</label>
      <textarea
        v-model="question"
        placeholder="请描述您想咨询的人生大事..."
        class="textarea textarea-bordered textarea-primary w-full h-24"
      ></textarea>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="alert alert-error mb-6">
      <span>{{ error }}</span>
    </div>

    <!-- 操作按钮 -->
    <div class="flex gap-4">
      <button @click="emit('back')" class="btn btn-ghost flex-1">返回</button>
      <button @click="submit" class="btn btn-secondary flex-1">开始推演</button>
    </div>
  </div>
</template>
