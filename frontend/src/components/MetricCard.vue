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
  background: var(--color-bg-card);
  backdrop-filter: blur(8px);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  border-color: var(--color-primary);
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 4px; height: 100%;
  transition: background-color 0.3s;
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
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.icon-wrapper svg) {
  width: 28px;
  height: 28px;
  color: #fff;
  filter: drop-shadow(0 0 5px rgba(255,255,255,0.3));
}

/* Color Variants */
.metric-card.pressure::before { background-color: var(--color-primary); }
.metric-card.pressure .icon-wrapper { color: var(--color-primary); }

.metric-card.microseismic::before { background-color: var(--color-warning); }
.metric-card.microseismic .icon-wrapper { color: var(--color-warning); }

.metric-card.deformation::before { background-color: var(--color-success); }
.metric-card.deformation .icon-wrapper { color: var(--color-success); }

.metric-card.alarms::before { background-color: var(--color-danger); }
.metric-card.alarms .icon-wrapper { color: var(--color-danger); }

.text-wrapper h3 { 
  margin: 0 0 0.4rem 0; 
  color: var(--color-text-muted); 
  font-size: 0.9rem; 
  font-weight: 500; 
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.text-wrapper .value { 
  font-size: 1.8rem; 
  font-weight: 700; 
  color: var(--color-text-main); 
  margin: 0; 
  line-height: 1.2;
}

.text-wrapper .value span { 
  font-size: 0.9rem; 
  color: var(--color-text-muted); 
  margin-left: 0.25rem; 
  font-weight: 400;
}
</style>
