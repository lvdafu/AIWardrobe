# 👕 AI Smart Wardrobe

**Your Personal AI Stylist & Wardrobe Manager**

[English](./README.md) | [简体中文](./README.zh-CN.md)

AI Smart Wardrobe is an AI-powered wardrobe manager that helps you upload clothing photos, remove backgrounds, classify garments, and generate outfit recommendations based on weather and style preferences.

## Introduction

AI Smart Wardrobe combines computer vision and large language models to build a practical personal styling workflow. It is designed for quick wardrobe digitization, daily outfit planning, and a responsive cross-device experience.

## Features

| Feature | Description |
| --- | --- |
| Smart Upload | Upload clothing photos, remove backgrounds with `rembg`, and analyze category, color, and style with AI vision models. |
| Weather-Based Styling | Integrates with the QWeather API to generate outfit suggestions based on current conditions. |
| Digital Wardrobe | Browse, search, and manage your clothing items in a structured wardrobe view. |
| AI Recommendations | Supports Gemini and OpenAI-style model providers for personalized outfit generation. |
| Responsive UI | Optimized for desktop, tablet, and mobile with a modern Tailwind CSS interface. |

## Demo

> The frontend has been redesigned with Tailwind CSS for a cleaner, more immersive responsive UI.

| Demo Areas | Description |
| --- | --- |
| New Item Entry | Upload via camera or gallery with a guided flow. |
| Wardrobe View | Browse by category and search quickly. |
| AI Recommendation | Generate weather-aware outfit suggestions. |
| Outfit Detail | Inspect clothing and outfit details clearly. |

## Tech Stack

### Frontend

- React
- Vite
- Tailwind CSS

### Backend & AI

- FastAPI
- SQLite
- Google Gemini / OpenAI-compatible APIs

## Getting Started

### Prerequisites

- Node.js `v20+`
- Python `v3.10+`
- API keys:
  - [Google Gemini API Key](https://aistudio.google.com/app/apikey) or an OpenAI-compatible API key
  - [QWeather API Key](https://console.qweather.com)

### 1. Clone the repository

```bash
git clone https://github.com/leoz9/AIWardrobe.git
cd AIWardrobe
```

### 2. Configure environment variables

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and fill in your API keys and settings
```

### 3. Install dependencies for the first run

`start.sh` and `start.bat` expect `backend/venv` and `frontend/node_modules` to exist, so install dependencies once before using the startup scripts.

**Backend**

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

**Frontend**

```bash
cd frontend
npm install
cd ..
```

### 4. Start the project

**macOS / Linux**

```bash
chmod +x start.sh
./start.sh
```

**Windows**

```cmd
start.bat
```

After startup:

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Manual start

If you want to run frontend and backend separately:

```bash
# Terminal 1: backend
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --reload --port 8000
```

```bash
# Terminal 2: frontend
cd frontend
npm run dev
```

## Docker Deployment

The repository now defaults to building locally from the current codebase, so your latest frontend and backend changes are included immediately. A prebuilt GitHub Container Registry image is still available if you only want a quick trial.

### Quick Start

```bash
# 1) Configure environment variables
cp backend/.env.example backend/.env

# 2) Build and run locally
docker build -t aiwardrobe:local .
docker run -d --name ai_wardrobe -p 8000:8000 \
  --env-file backend/.env \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/data:/app/backend/data \
  aiwardrobe:local
```

To use the remote image instead:

```bash
docker pull ghcr.io/leoz9/aiwardrobe:latest
docker run -d --name ai_wardrobe -p 8000:8000 \
  --env-file backend/.env \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  -v $(pwd)/backend/data:/app/backend/data \
  ghcr.io/leoz9/aiwardrobe:latest
```

### Docker Compose

#### Requirements

- [Docker](https://www.docker.com/)
- Docker Compose Plugin

#### Steps

1. Clone the project and configure the environment:

```bash
git clone https://github.com/leoz9/AIWardrobe.git
cd AIWardrobe
cd backend && cp .env.example .env
# Edit .env and fill in your API keys
```

2. Start the application:

```bash
cd ..
docker compose up --build -d
```

3. Access the app:

- Web app: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

Data is persisted in `backend/data` and `backend/uploads`.

## Star History

[Star History Chart](https://www.star-history.com/#leoz9/AIWardrobe&type=date&legend=top-left)

## Contributing

Contributions are welcome. If you find a bug or have an improvement idea, open an issue or submit a pull request.

## License

[MIT](LICENSE)
