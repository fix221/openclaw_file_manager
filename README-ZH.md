# Openclaw_File_Manager

[EN](https://github.com/fix221/openclaw_file_manager/blob/main/README.md)

## 项目描述

这是一个为 Openclaw 定制开发的简易文件管理工具，方便上传和下载文件

![Static Badge](https://img.shields.io/badge/最后更新-2026年4月-blue)![Static Badge](https://img.shields.io/badge/Openclaw-最新版本-green)

## 功能特性

- 基于 Web 的文件管理界面
- 支持拖拽上传文件
- 文件下载功能
- 实时文件列表更新
- 一键复制下载链接
- 删除文件前确认
- 可视化文件类型图标
- 响应式设计和深色主题

## 快速开始

### 环境要求

- Python 3.8+
- Flask

### 安装

```bash
pip install flask
```

### 运行应用

```bash
python app.py
```

应用将在 `http://0.0.0.0:8080` 启动

### 配置

默认目录：

- 下载区：`./downloads`
- 上传区：`./uploads`

如需修改路径，可在 `app.py` 中更改

## API 接口

| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/files/{folder}` | 获取文件夹中的文件列表 |
| POST | `/api/upload` | 上传文件 |
| POST | `/api/delete` | 删除文件 |
| GET | `/api/download/{filename}` | 下载文件 |

## 使用说明

1. 打开网页界面
2. 使用上传按钮上传文件
3. 从下载区下载文件
4. 复制可分享的下载链接

## 贡献指南

欢迎提交 Issue 或 Fork 项目来改进

## 许可证

MIT License