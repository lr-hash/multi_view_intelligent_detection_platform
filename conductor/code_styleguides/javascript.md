# JavaScript/Vue Code Style Guide

## 1. 基础规范
- 使用 2 个空格进行缩进。
- 强制使用分号 `;` 结尾。
- 使用单引号 `'` 括起字符串，除非为了避免转义。

## 2. Vue 3 规范
- **Composition API**：统一使用 `<script setup>` 语法。
- **组件命名**：文件名使用 `PascalCase`（如 `MyComponent.vue`），在模板中使用 `kebab-case`（如 `<my-component />`）。
- **Props 定义**：使用 `defineProps` 并明确类型定义。

## 3. 变量命名
- 变量与函数：使用 `camelCase`（小驼峰命名法）。
- 组件与类：使用 `PascalCase`。

## 4. 现代语法
- 优先使用 `const` 和 `let`，禁止使用 `var`。
- 优先使用箭头函数 `() => {}`。
- 充分利用模板字符串 `` `text ${value}` ``。
