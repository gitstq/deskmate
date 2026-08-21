# 贡献指南 / Contributing Guide

感谢你对 DeskMate 的兴趣！我们欢迎各种形式的贡献。

Thank you for your interest in DeskMate! We welcome contributions in all forms.

## 🐛 报告 Bug / Report Bugs

请在 Issue 中包含以下信息 / Please include the following in your issue:
- 操作系统及版本 / OS and version
- Python 版本 / Python version
- DeskMate 版本 / DeskMate version
- 复现步骤 / Steps to reproduce
- 预期行为与实际行为 / Expected vs actual behavior

## ✨ 提交新功能 / Submit New Features

1. 先开 Issue 讨论功能设计 / Open an issue first to discuss the feature design
2. Fork 仓库并创建特性分支 / Fork the repo and create a feature branch
3. 遵循代码规范 / Follow code conventions
4. 添加必要的测试 / Add necessary tests
5. 提交 PR / Submit a Pull Request

## 🐾 添加新宠物角色 / Add New Pet Species

1. 在 `deskmate/pets/` 下创建新文件 / Create a new file under `deskmate/pets/`
2. 继承 `BasePet` 并实现 `draw()` 方法 / Inherit `BasePet` and implement the `draw()` method
3. 在 `deskmate/pets/__init__.py` 中注册 / Register in `deskmate/pets/__init__.py`
4. 添加对应的显示名称 / Add corresponding display name
5. 确保程序化绘制，不依赖外部图片 / Ensure programmatic drawing, no external images

## 📝 代码规范 / Code Conventions

- Python: 遵循 PEP 8 / Follow PEP 8
- 注释：核心逻辑必须有中英文注释 / Core logic must have Chinese-English comments
- 提交信息：遵循 Angular 规范 / Follow Angular commit convention:
  - `feat:` 新功能 / New feature
  - `fix:` 修复 / Bug fix
  - `docs:` 文档 / Documentation
  - `style:` 格式 / Formatting
  - `refactor:` 重构 / Refactor
  - `test:` 测试 / Testing
  - `chore:` 构建/工具 / Build/tools

## 🧪 运行测试 / Run Tests

```bash
python -m pytest tests/ -v
# 或 / or
python -m unittest discover tests/ -v
```

## 📄 许可证 / License

提交代码即表示你同意以 MIT 协议授权你的贡献。
By submitting code, you agree to license your contribution under the MIT License.
