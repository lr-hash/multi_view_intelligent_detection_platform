<template>
  <div class="metric-card" :class="type">
    <div class="icon-wrapper">
      <slot name="icon"></slot>
    </div>
    <div class="text-wrapper">
      <h3>{{ title }}</h3>
      <p class="value">
        {{ value }} <span v-if="unit">{{ unit }}</span>
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  unit: String,
  type: String // pressure, microseismic, deformation, alarms
});
</script>

<style scoped>
.metric-card {
  background-color: #1a2952;
  border: 1px solid #2a3f78;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
}
.metric-card:hover {
  transform: translateY(-2px);
}
.icon-wrapper {
  flex-shrink: 0;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1.5rem;
  background-color: #334155;
}
:deep(.icon-wrapper svg) {
  width: 28px;
  height: 28px;
  color: #fff;
}
/* 颜色变体 */
.pressure .icon-wrapper { background-color: #007bff; }
.microseismic .icon-wrapper { background-color: #ffc107; }
.deformation .icon-wrapper { background-color: #28a745; }
.alarms .icon-wrapper { background-color: #dc3545; }

.text-wrapper h3 { margin: 0 0 0.5rem 0; color: #c0c5d6; font-size: 1rem; font-weight: 400; }
.text-wrapper .value { font-size: 1.8rem; font-weight: bold; color: #fff; margin: 0; }
.text-wrapper .value span { font-size: 1rem; color: #c0c5d6; margin-left: 0.25rem; }
</style>
