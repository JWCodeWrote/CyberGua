<script setup>
/**
 * 结果展示组件
 * 显示占卜结果和 AI 分析
 */
import { computed } from "vue";

const props = defineProps({
  result: Object,
  mode: String,
});

const emit = defineEmits(["restart", "home"]);

// 是否有有效结果
const hasResult = computed(() => {
  return props.result && (props.result.hexagram || props.result.bazi);
});

// 卦象信息
const hexagram = computed(() => props.result?.hexagram || {});

// 八字信息 (详细版)
const bazi = computed(() => props.result?.bazi || {});

// 风水信息 (详细版)
const fengshui = computed(() => props.result?.fengshui || {});

// AI 分析
const aiAnalysis = computed(() => {
  return props.result?.ai_analysis || props.result?.ai_report || "暂无 AI 分析";
});
</script>

<template>
  <div class="fade-in-up">
    <!-- 错误状态 -->
    <div v-if="!hasResult" class="text-center py-12">
      <div class="text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-error mb-4">占卜失败</h2>
      <p class="text-base-content/60 mb-8">{{ result?.error || "未知错误" }}</p>
      <button @click="emit('home')" class="btn btn-primary">返回首页</button>
    </div>

    <!-- 成功结果 -->
    <div v-else>
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gold mb-2">
          {{ mode === "simple" ? "卦象解读" : "命运报告" }}
        </h2>
        <p class="text-base-content/60">
          {{ result.success ? "AI 分析完成" : "AI 暂不可用，仅展示算法结果" }}
        </p>
      </div>

      <!-- 卦象卡片 -->
      <div class="gua-card rounded-2xl p-6 mb-6">
        <h3 class="text-lg font-bold text-primary mb-4">☯ 卦象</h3>

        <div class="grid grid-cols-3 gap-4 text-center mb-4">
          <div>
            <div class="text-xs text-base-content/50 mb-1">本卦</div>
            <div class="text-xl font-bold text-primary">
              {{ hexagram.original?.name || "-" }}
            </div>
          </div>
          <div>
            <div class="text-xs text-base-content/50 mb-1">互卦</div>
            <div class="text-xl font-bold">
              {{ hexagram.mutual?.name || "-" }}
            </div>
          </div>
          <div>
            <div class="text-xs text-base-content/50 mb-1">变卦</div>
            <div class="text-xl font-bold text-secondary">
              {{ hexagram.changed?.name || "-" }}
            </div>
          </div>
        </div>

        <div class="divider opacity-30"></div>

        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-base-content/50">体卦：</span>
            <span class="font-medium"
              >{{ hexagram.ti_gua?.name }} ({{
                hexagram.ti_gua?.element
              }})</span
            >
          </div>
          <div>
            <span class="text-base-content/50">用卦：</span>
            <span class="font-medium"
              >{{ hexagram.yong_gua?.name }} ({{
                hexagram.yong_gua?.element
              }})</span
            >
          </div>
          <div class="col-span-2">
            <span class="text-base-content/50">体用关系：</span>
            <span
              class="font-bold"
              :class="{
                'text-success':
                  hexagram.ti_yong_relation?.includes('体克用') ||
                  hexagram.ti_yong_relation?.includes('用生体'),
                'text-warning': hexagram.ti_yong_relation?.includes('比和'),
                'text-error': hexagram.ti_yong_relation?.includes('用克体'),
              }"
            >
              {{ hexagram.ti_yong_relation }}
            </span>
            <span class="text-base-content/60 ml-2"
              >- {{ hexagram.interpretation }}</span
            >
          </div>
        </div>
      </div>

      <!-- 八字卡片 (详细版) -->
      <div
        v-if="mode === 'detailed' && bazi.four_pillars"
        class="gua-card rounded-2xl p-6 mb-6"
      >
        <h3 class="text-lg font-bold text-secondary mb-4">📜 八字命盘</h3>

        <div class="grid grid-cols-4 gap-2 text-center mb-4">
          <div class="bg-base-300/30 rounded-lg p-3">
            <div class="text-xs text-base-content/50 mb-1">年柱</div>
            <div class="text-xl font-bold">{{ bazi.four_pillars.year }}</div>
          </div>
          <div class="bg-base-300/30 rounded-lg p-3">
            <div class="text-xs text-base-content/50 mb-1">月柱</div>
            <div class="text-xl font-bold">{{ bazi.four_pillars.month }}</div>
          </div>
          <div class="bg-base-300/30 rounded-lg p-3">
            <div class="text-xs text-base-content/50 mb-1">日柱</div>
            <div class="text-xl font-bold text-primary">
              {{ bazi.four_pillars.day }}
            </div>
          </div>
          <div class="bg-base-300/30 rounded-lg p-3">
            <div class="text-xs text-base-content/50 mb-1">时柱</div>
            <div class="text-xl font-bold">{{ bazi.four_pillars.hour }}</div>
          </div>
        </div>

        <div class="text-sm space-y-2">
          <div>
            <span class="text-base-content/50">日主：</span>
            <span class="font-bold text-primary">{{ bazi.day_master }}</span>
            <span class="text-base-content/60">
              ({{ bazi.day_master_wuxing }})</span
            >
            <span
              class="badge badge-sm ml-2"
              :class="
                bazi.strength === '身强' ? 'badge-success' : 'badge-warning'
              "
            >
              {{ bazi.strength }}
            </span>
          </div>
          <div>
            <span class="text-base-content/50">喜用神：</span>
            <span class="font-medium text-success">{{
              bazi.favorable_elements?.join("、")
            }}</span>
          </div>
          <div>
            <span class="text-base-content/50">忌神：</span>
            <span class="font-medium text-error">{{
              bazi.unfavorable_elements?.join("、")
            }}</span>
          </div>
        </div>
      </div>

      <!-- 风水卡片 (详细版) -->
      <div
        v-if="mode === 'detailed' && fengshui.ming_gua"
        class="gua-card rounded-2xl p-6 mb-6"
      >
        <h3 class="text-lg font-bold text-accent mb-4">🏠 风水方位</h3>

        <div class="grid grid-cols-2 gap-4 text-sm mb-4">
          <div>
            <span class="text-base-content/50">本命卦：</span>
            <span class="font-bold">{{ fengshui.ming_gua.gua_name }}</span>
            <span class="badge badge-sm badge-outline ml-2">{{
              fengshui.ming_gua.life_group
            }}</span>
          </div>
          <div>
            <span class="text-base-content/50">最佳方位：</span>
            <span class="font-bold text-primary">{{
              fengshui.ming_gua.best_direction
            }}</span>
          </div>
          <div>
            <span class="text-base-content/50">流年财位：</span>
            <span class="font-bold text-success">{{
              fengshui.flying_stars?.wealth_position
            }}</span>
          </div>
          <div>
            <span class="text-base-content/50">流年桃花：</span>
            <span class="font-bold text-secondary">{{
              fengshui.flying_stars?.romance_position
            }}</span>
          </div>
        </div>

        <div class="text-xs text-base-content/50">
          <span class="text-success">吉方：</span>
          {{ fengshui.flying_stars?.auspicious?.join("、") }}
        </div>
      </div>

      <!-- AI 分析 -->
      <div class="gua-card rounded-2xl p-6 mb-6">
        <h3 class="text-lg font-bold text-primary mb-4">🤖 AI 解读</h3>
        <div class="prose prose-sm prose-invert max-w-none">
          <pre
            class="whitespace-pre-wrap font-sans text-base-content/80 bg-transparent p-0"
            >{{ aiAnalysis }}</pre
          >
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex gap-4">
        <button @click="emit('home')" class="btn btn-ghost flex-1">
          返回首页
        </button>
        <button @click="emit('restart')" class="btn btn-primary flex-1">
          重新占卜
        </button>
      </div>
    </div>
  </div>
</template>
