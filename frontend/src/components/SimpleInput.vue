<script setup>
/**
 * 简单版输入组件
 * 输入三个数字 + 问题
 */
import { ref } from "vue";
import { predictSimple } from "../api";

const emit = defineEmits(["submit", "loading", "back"]);

const num1 = ref(null);
const num2 = ref(null);
const num3 = ref(null);
const question = ref("");
const error = ref("");

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
    const result = await predictSimple(
      [parseInt(num1.value), parseInt(num2.value), parseInt(num3.value)],
      question.value,
    );
    emit("submit", result);
  } catch (e) {
    error.value = e.response?.data?.detail || "请求失败，请确保后端服务已启动";
    emit("submit", { error: error.value, success: false });
  }
}
</script>

<template>
  <div class="fade-in-up max-w-xl mx-auto">
    <!-- 标题 -->
    <div class="text-center mb-8">
      <h2 class="text-3xl font-bold text-gold mb-2">快速占卜</h2>
      <p class="text-base-content/60">凭直觉输入三个数字 (1-64)</p>
    </div>

    <!-- 数字输入 -->
    <div class="gua-card rounded-2xl p-6 mb-6">
      <label class="block text-sm font-medium text-primary mb-4">☯ 报数</label>

      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="form-control">
          <label class="label">
            <span class="label-text text-base-content/50">下卦</span>
          </label>
          <input
            type="number"
            v-model="num1"
            min="1"
            max="64"
            placeholder="1-64"
            class="input input-bordered input-primary text-center text-2xl"
          />
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text text-base-content/50">上卦</span>
          </label>
          <input
            type="number"
            v-model="num2"
            min="1"
            max="64"
            placeholder="1-64"
            class="input input-bordered input-primary text-center text-2xl"
          />
        </div>
        <div class="form-control">
          <label class="label">
            <span class="label-text text-base-content/50">动爻</span>
          </label>
          <input
            type="number"
            v-model="num3"
            min="1"
            max="64"
            placeholder="1-64"
            class="input input-bordered input-primary text-center text-2xl"
          />
        </div>
      </div>

      <div class="text-center text-xs text-base-content/40">
        💡 闭上眼睛，想着问题，凭第一直觉报数
      </div>
    </div>

    <!-- 问题输入 -->
    <div class="gua-card rounded-2xl p-6 mb-6">
      <label class="block text-sm font-medium text-primary mb-4">☯ 问题</label>
      <textarea
        v-model="question"
        placeholder="请描述您想占卜的事情..."
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
      <button @click="submit" class="btn btn-primary flex-1">开始占卜</button>
    </div>
  </div>
</template>
