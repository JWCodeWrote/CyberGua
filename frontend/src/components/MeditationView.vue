<script setup>
/**
 * 冥想引导组件
 * 引导用户进入放松状态后报数
 */
import { ref, onMounted, onUnmounted } from "vue";

const emit = defineEmits(["complete", "skip"]);

const phase = ref("intro"); // intro, breathing, complete
const breathCount = ref(0);
const maxBreaths = 3;
let breathInterval = null;

function startBreathing() {
  phase.value = "breathing";
  breathCount.value = 0;

  breathInterval = setInterval(() => {
    breathCount.value++;
    if (breathCount.value >= maxBreaths) {
      clearInterval(breathInterval);
      phase.value = "complete";
      setTimeout(() => {
        emit("complete");
      }, 1500);
    }
  }, 4000); // 每次呼吸4秒
}

function skip() {
  if (breathInterval) {
    clearInterval(breathInterval);
  }
  emit("skip");
}

onUnmounted(() => {
  if (breathInterval) {
    clearInterval(breathInterval);
  }
});
</script>

<template>
  <div
    class="fade-in-up min-h-[60vh] flex flex-col items-center justify-center"
  >
    <!-- 介绍阶段 -->
    <div v-if="phase === 'intro'" class="text-center">
      <div class="text-8xl mb-8">🧘</div>
      <h2 class="text-3xl font-bold text-gold mb-4">冥想引导</h2>
      <p class="text-base-content/70 mb-8 max-w-md mx-auto">
        在起卦之前，请先让心灵沉淀。<br />
        闭上眼睛，深呼吸三次，让思绪回归当下。
      </p>

      <div class="space-x-4">
        <button @click="startBreathing" class="btn btn-primary btn-lg">
          开始冥想
        </button>
        <button @click="skip" class="btn btn-ghost">跳过</button>
      </div>
    </div>

    <!-- 呼吸阶段 -->
    <div v-if="phase === 'breathing'" class="text-center">
      <div class="relative w-48 h-48 mx-auto mb-8">
        <!-- 呼吸动画圆环 -->
        <div
          class="absolute inset-0 rounded-full border-4 border-primary/30"
        ></div>
        <div
          class="absolute inset-0 rounded-full border-4 border-primary breathing"
        ></div>
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-6xl">☯</span>
        </div>
      </div>

      <h2 class="text-2xl font-bold text-primary mb-2">深呼吸</h2>
      <p class="text-base-content/70 mb-4">吸气... 呼气...</p>

      <div class="flex justify-center gap-2 mb-8">
        <template v-for="i in maxBreaths" :key="i">
          <div
            class="w-3 h-3 rounded-full transition-colors"
            :class="i <= breathCount ? 'bg-primary' : 'bg-base-content/20'"
          ></div>
        </template>
      </div>

      <button @click="skip" class="btn btn-ghost btn-sm">跳过冥想</button>
    </div>

    <!-- 完成阶段 -->
    <div v-if="phase === 'complete'" class="text-center">
      <div class="text-8xl mb-8">✨</div>
      <h2 class="text-3xl font-bold text-gold mb-4">心神已定</h2>
      <p class="text-base-content/70">现在，请凭直觉报出三个数字...</p>
    </div>
  </div>
</template>
