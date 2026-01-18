<script setup>
import { ref } from "vue";
import ModeSelection from "./components/ModeSelection.vue";
import SimpleInput from "./components/SimpleInput.vue";
import DetailedInput from "./components/DetailedInput.vue";
import ResultView from "./components/ResultView.vue";
import MeditationView from "./components/MeditationView.vue";

// 应用状态
const currentView = ref("mode-selection"); // mode-selection, meditation, simple-input, detailed-input, result
const selectedMode = ref(null); // 'simple' | 'detailed'
const result = ref(null);
const isLoading = ref(false);

// 选择模式
function selectMode(mode) {
  selectedMode.value = mode;
  if (mode === "simple") {
    currentView.value = "meditation";
  } else {
    currentView.value = "detailed-input";
  }
}

// 冥想完成
function onMeditationComplete() {
  currentView.value = "simple-input";
}

// 跳过冥想
function onSkipMeditation() {
  currentView.value = "simple-input";
}

// 预测完成
function onPredictComplete(data) {
  result.value = data;
  isLoading.value = false;
  currentView.value = "result";
}

// 开始加载
function onStartLoading() {
  isLoading.value = true;
}

// 返回首页
function goHome() {
  currentView.value = "mode-selection";
  selectedMode.value = null;
  result.value = null;
  isLoading.value = false;
}

// 重新占卜
function restart() {
  if (selectedMode.value === "simple") {
    currentView.value = "meditation";
  } else {
    currentView.value = "detailed-input";
  }
  result.value = null;
}
</script>

<template>
  <div class="min-h-screen">
    <!-- 头部导航 -->
    <header
      class="navbar bg-base-100/80 backdrop-blur-lg border-b border-primary/20 sticky top-0 z-50"
    >
      <div class="flex-1">
        <button
          @click="goHome"
          class="btn btn-ghost text-xl text-gold font-bold"
        >
          ☯ CyberGua 赛博卦
        </button>
      </div>
      <div class="flex-none">
        <span class="text-xs text-base-content/50">Cyber Oracle v1.0</span>
      </div>
    </header>

    <!-- 主要内容区 -->
    <main class="container mx-auto px-4 py-8 max-w-4xl">
      <!-- 加载遮罩 -->
      <div
        v-if="isLoading"
        class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center"
      >
        <div class="text-center">
          <div
            class="loading loading-ring loading-lg text-primary loading-glow"
          ></div>
          <p class="mt-4 text-primary text-lg">正在推演卦象...</p>
          <p class="text-sm text-base-content/50 mt-2">AI 正在分析命理信息</p>
        </div>
      </div>

      <!-- 模式选择 -->
      <ModeSelection
        v-if="currentView === 'mode-selection'"
        @select="selectMode"
      />

      <!-- 冥想引导 -->
      <MeditationView
        v-if="currentView === 'meditation'"
        @complete="onMeditationComplete"
        @skip="onSkipMeditation"
      />

      <!-- 简单版输入 -->
      <SimpleInput
        v-if="currentView === 'simple-input'"
        @submit="onPredictComplete"
        @loading="onStartLoading"
        @back="() => (currentView = 'meditation')"
      />

      <!-- 详细版输入 -->
      <DetailedInput
        v-if="currentView === 'detailed-input'"
        @submit="onPredictComplete"
        @loading="onStartLoading"
        @back="goHome"
      />

      <!-- 结果展示 -->
      <ResultView
        v-if="currentView === 'result'"
        :result="result"
        :mode="selectedMode"
        @restart="restart"
        @home="goHome"
      />
    </main>

    <!-- 页脚 -->
    <footer class="footer footer-center p-4 text-base-content/30 text-xs">
      <p>CyberGua 赛博卦 · 命运可算 · 未来可期</p>
    </footer>
  </div>
</template>
