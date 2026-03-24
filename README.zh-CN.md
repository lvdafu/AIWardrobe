# 👕 AI 智能衣柜

**你的个人 AI 穿搭顾问与衣橱管理助手**

[English](./README.md) | [简体中文](./README.zh-CN.md)

AI Smart Wardrobe 是一个基于 AI 的个人智能衣柜管理系统。它支持上传衣物图片、自动去背景、识别服装类别，并结合天气与风格偏好生成穿搭建议。

## 简介

AI Smart Wardrobe 将计算机视觉与大语言模型结合起来，帮助你快速数字化衣橱、管理衣物，并生成更实用的每日穿搭方案，适合桌面端和移动端使用。

## 核心特性

| 特性 | 描述 |
| --- | --- |
| 智能上传 | 上传衣服照片后，使用 `rembg` 自动去背景，并通过视觉模型识别类别、颜色和风格。 |
| 天气穿搭 | 集成和风天气 API，根据实时天气生成更合适的穿搭建议。 |
| 虚拟衣柜 | 以结构化方式浏览、搜索和管理所有衣物。 |
| AI 推荐 | 支持 Gemini 和 OpenAI 风格接口，用于生成个性化穿搭方案。 |
| 响应式界面 | 基于 Tailwind CSS，适配桌面、平板和手机。 |

## 运行演示

> 前端已经使用 Tailwind CSS 完成重构，界面更加现代、响应式也更完整。

| 演示模块 | 描述 |
| --- | --- |
| 录入新衣 | 支持拍照或从图库上传，流程更清晰。 |
| 我的衣橱 | 可按分类浏览并快速搜索。 |
| AI 推荐 | 生成结合天气的穿搭建议。 |
| 穿搭详情 | 更清楚地展示单品和搭配细节。 |

## 技术栈

### 前端

- React
- Vite
- Tailwind CSS

### 后端与 AI

- FastAPI
- SQLite
- Google Gemini / OpenAI 兼容接口

## 快速开始

### 前置要求

- Node.js `v20+`
- Python `v3.10+`
- API Key：
  - [Google Gemini API Key](https://aistudio.google.com/app/apikey) 或 OpenAI 兼容接口 Key
  - [和风天气 API Key](https://console.qweather.com)

### 1. 克隆仓库

```bash
git clone https://github.com/leoz9/AIWardrobe.git
cd AIWardrobe
```

### 2. 配置环境变量

```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入你的 API Key 和相关配置
```

### 3. 首次安装依赖

`start.sh` 和 `start.bat` 会直接使用 `backend/venv` 与 `frontend/node_modules`，因此首次运行前需要先安装依赖。

**后端**

```bash
cd backend
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate

pip install -r requirements.txt
cd ..
```

**前端**

```bash
cd frontend
npm install
cd ..
```

### 4. 启动项目

**macOS / Linux**

```bash
chmod +x start.sh
./start.sh
```

**Windows**

```cmd
start.bat
```

启动后访问：

- 前端页面: [http://localhost:5173](http://localhost:5173)
- 后端 API: [http://localhost:8000](http://localhost:8000)
- API 文档: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. 手动启动

如果你想分别控制前后端，可以开两个终端：

```bash
# 终端 1：后端
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --reload --port 8000
```

```bash
# 终端 2：前端
cd frontend
npm run dev
```

## Docker 部署

当前仓库默认通过本地 `Dockerfile` 构建镜像，因此你最新的前后端修改会直接包含在镜像中。如果你只是想快速体验，也可以使用 GitHub Container Registry 中的预构建镜像。

### 快速开始

```bash
# 1) 配置环境变量
cp backend/.env.example backend/.env

# 2) 本地构建并启动
docker build -t aiwardrobe:local .
docker run -d --name ai_wardrobe -p 8000:8000 \
  --env-file backend/.env \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/data:/app/backend/data \
  aiwardrobe:local
```

如果你想直接使用远端镜像：

```bash
docker pull ghcr.io/leoz9/aiwardrobe:latest
docker run -d --name ai_wardrobe -p 8000:8000 \
  --env-file backend/.env \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/data:/app/backend/data \
  ghcr.io/leoz9/aiwardrobe:latest
```

### Docker Compose

#### 前置要求

- [Docker](https://www.docker.com/)
- Docker Compose Plugin

#### 部署步骤

1. 克隆项目并配置环境变量：

```bash
git clone https://github.com/leoz9/AIWardrobe.git
cd AIWardrobe
cd backend && cp .env.example .env
# 编辑 .env，填入你的 API Key
```

2. 启动应用：

```bash
cd ..
docker compose up --build -d
```

3. 访问项目：

- Web 应用: [http://localhost:8000](http://localhost:8000)
- API 文档: [http://localhost:8000/docs](http://localhost:8000/docs)
- 健康检查: [http://localhost:8000/health](http://localhost:8000/health)

数据会持久化保存在 `backend/data` 和 `backend/uploads` 目录中。

## Star History

[Star History Chart](https://www.star-history.com/#leoz9/AIWardrobe&type=date&legend=top-left)

## 贡献

欢迎提交 Issue 或 Pull Request 来帮助改进这个项目。

## 许可证

[MIT](LICENSE)
