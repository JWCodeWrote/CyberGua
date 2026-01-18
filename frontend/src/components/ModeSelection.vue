<script setup>
/**
 * 模式选择组件
 * 让用户选择简单版或详细版
 */
defineEmits(["select"]);
</script>

<template>
  <div class="fade-in-up">
    <!-- 标题区 -->
    <div class="text-center mb-12">
      <h1 class="text-4xl md:text-5xl font-bold text-gold mb-4">赛博玄学</h1>
      <p class="text-base-content/70 text-lg">
        融合东方玄学与现代 AI 的命理预测系统
      </p>
    </div>

    <!-- 模式卡片 -->
    <div class="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
      <!-- 简单版 -->
      <div
        @click="$emit('select', 'simple')"
        class="gua-card rounded-2xl p-8 cursor-pointer group"
      >
        <div class="text-center">
          <div class="text-6xl mb-4 group-hover:scale-110 transition-transform">
            🎲
          </div>
          <h2 class="text-2xl font-bold text-primary mb-2">简单版</h2>
          <p class="text-sm text-base-content/60 mb-4">快速决策 · 单一事件</p>

          <div class="divider divider-primary opacity-30"></div>

          <ul class="text-left text-sm space-y-2 text-base-content/70">
            <li class="flex items-center gap-2">
              <span class="text-primary">☯</span> 梅花易数起卦
            </li>
            <li class="flex items-center gap-2">
              <span class="text-primary">☯</span> 冥想引导 + 报数
            </li>
            <li class="flex items-center gap-2">
              <span class="text-primary">☯</span> AI 快速解读
            </li>
          </ul>

          <div class="mt-6">
            <span class="badge badge-primary badge-outline">适合日常决策</span>
          </div>
        </div>
      </div>

      <!-- 详细版 -->
      <div
        @click="$emit('select', 'detailed')"
        class="gua-card rounded-2xl p-8 cursor-pointer group"
      >
        <div class="text-center">
          <div class="text-6xl mb-4 group-hover:scale-110 transition-transform">
            📜
          </div>
          <h2 class="text-2xl font-bold text-secondary mb-2">详细版</h2>
          <p class="text-sm text-base-content/60 mb-4">人生战略 · 综合命理</p>

          <div class="divider divider-secondary opacity-30"></div>

          <ul class="text-left text-sm space-y-2 text-base-content/70">
            <li class="flex items-center gap-2">
              <span class="text-secondary">☯</span> 八字定盘 (能否做?)
            </li>
            <li class="flex items-center gap-2">
              <span class="text-secondary">☯</span> 梅花起卦 (何时做?)
            </li>
            <li class="flex items-center gap-2">
              <span class="text-secondary">☯</span> 九宫飞星 (在哪做?)
            </li>
          </ul>

          <div class="mt-6">
            <span class="badge badge-secondary badge-outline"
              >适合重大决策</span
            >
          </div>
        </div>
      </div>
    </div>

    <!-- 提示信息 -->
    <div class="text-center mt-12 text-base-content/40 text-sm">
      <p>⚡ 本地 AI 运行 · 隐私安全 · 无需联网</p>
    </div>
  </div>
</template>
