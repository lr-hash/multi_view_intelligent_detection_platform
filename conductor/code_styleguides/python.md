# Python Code Style Guide

## 1. 基础规范
- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 代码风格指南。
- 使用 4 个空格进行缩进。
- 每行代码长度限制在 79-88 字符以内。

## 2. 命名约定
- 函数与变量名：使用 `snake_case`（蛇形命名法）。
- 类名：使用 `PascalCase`（大驼峰命名法）。
- 常量：使用 `UPPER_SNAKE_CASE`（大写蛇形命名法）。

## 3. Flask & SQLAlchemy 规范
- **模型定义**：模型类应定义在 `models.py` 中。
- **视图逻辑**：保持路由处理函数（View Functions）简洁，将复杂逻辑抽离到 `services.py`。
- **类型提示**：鼓励在函数签名中使用 Type Hints，以提高代码的可维护性和 IDE 友好度。

## 4. 文档字符串 (Docstrings)
- 所有公共函数、类和方法都应包含 Google 风格的文档字符串，说明其功能、参数和返回值。
