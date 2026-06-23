# GuideForCoach

**A Moneyball scouting system powered by ML and AI agents** — find similar players and generate intelligent scouting reports.

---

## 🎯 What It Does

GuideForCoach combines machine learning and LLM-powered agents to help scouts discover similar players and generate detailed analysis reports. It processes player data, trains a similarity model, and runs an intelligent agent workflow that scouts, researches, and directs insights about any player.

---

## 🔄 System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     GuideForCoach API                        │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
         ┌──────▼──────┐           ┌────────▼────────┐
         │   Pipeline   │           │     Agent       │
         │   Endpoint   │           │    Endpoint     │
         └──────┬──────┘           └────────┬────────┘
                │                           │
    ┌───────────▼──────────┐    ┌──────────▼─────────┐
    │  1. Load & Clean     │    │ 1. Check Cache     │
    │  2. Train Model      │    │ 2. Validate Player │
    │  3. Save Artifacts   │    │ 3. Run Agent       │
    │                      │    │    • Scout         │
    │  ✓ Ready for use     │    │    • Research      │
    └──────────────────────┘    │    • Director      │
                                │ 4. Cache Result    │
                                │ 5. Save Report     │
                                └────────────────────┘
```

---

## 📦 Main Components

### 1. **ML Pipeline** (`/pipeline/run`)
Processes player data and trains a similarity engine:
- **Data Processing**: Clean and prepare player statistics
- **Model Training**: Scikit-learn NearestNeighbors (KNN) model
- **Artifact Storage**: Saves model, scaler, and dataset for inference

### 2. **Scouting Agent** (`/agent/scout`)
LangGraph-based workflow for intelligent player analysis:
- **Scout Node**: Gathers initial player information
- **Researcher Node**: Digs deeper into player metrics and comparisons
- **Director Node**: Synthesizes insights and generates final report
- **Caching**: Returns instant results on repeated queries
- **Rate Limiting**: 5 requests/minute per IP

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd guideforcoach

# Install dependencies
pip install -e .
```

### Running the Server

```bash
python main.py
```

Server runs on `http://localhost:8000`

### Health Check

```bash
curl http://localhost:8000/health
```

---

## 📡 API Endpoints

### Pipeline Endpoints

**POST** `/pipeline/run` — Trigger the ML pipeline
```bash
curl -X POST http://localhost:8000/pipeline/run
```

**Response:**
```json
{
  "status": "success",
  "message": "Pipeline completed successfully. Model is ready for inference."
}
```

### Agent Endpoints

**POST** `/agent/scout` — Scout a player and generate a report
```bash
curl -X POST http://localhost:8000/agent/scout \
  -H "Content-Type: application/json" \
  -d '{"player_name": "Matthis Abline"}'
```

**Response:**
```json
{
  "player_name": "Matthis Abline",
  "report": "...",
  "similar_players": [...],
  "cached": false
}
```

---

## 🔧 Configuration

Edit `src/config.py` to customize:
- Feature selection for similarity model
- Number of neighbors (`N_NEIGHBORS`)
- Distance metric (`METRIC`)
- Model paths and database paths

---

## 📁 Project Structure

```
guideforcoach/
├── api/
│   ├── main.py              # FastAPI app setup
│   ├── routers/
│   │   ├── pipeline.py      # Pipeline endpoints
│   │   └── agent.py         # Agent endpoints
│   ├── cache.py             # Response caching
│   ├── validators.py        # Input validation
│   └── schemas.py           # Request/response models
├── src/
│   ├── model.py             # SimilarityEngine (KNN)
│   ├── config.py            # Configuration
│   ├── preprocess.py        # Data preprocessing
│   └── agents/
│       └── graph.py         # LangGraph agent workflow
├── main.py                  # FastAPI server entry point
├── main_pipeline.py         # Pipeline orchestrator
├── resultfilecreate.py      # Report generation
└── reports/                 # Generated scouting reports
```

---

## ⚙️ How It Works

### Pipeline Flow

1. **Load Data**: Read player statistics from source
2. **Preprocess**: Clean, scale, and prepare features
3. **Train Model**: Fit KNN model on player embeddings
4. **Save Artifacts**: Store model, scaler, and dataset

### Agent Flow

1. **Cache Check**: Return cached result if player was already scouted
2. **Validation**: Verify player exists in dataset
3. **Agent Workflow**:
   - **Scout**: Extract player baseline metrics
   - **Researcher**: Find similar players and analyze patterns
   - **Director**: Synthesize findings into a comprehensive report
4. **Persist**: Cache result and save report to `reports/`

---

## 🔒 Features

- ✅ **Smart Caching**: Instant results on repeated queries
- ✅ **Rate Limiting**: Protect API from abuse (5 req/min)
- ✅ **Player Validation**: Reject unknown players before LLM calls
- ✅ **Persistent Reports**: All scouting reports saved as Markdown
- ✅ **Error Handling**: Graceful failures with descriptive messages

---

## 🛠️ Development

### Run Tests

```bash
pytest tests/
```

### Access API Docs

```
http://localhost:8000/docs     # Swagger UI
http://localhost:8000/redoc    # ReDoc
```

---

## 📝 License

MIT License

---

**Questions?** Check the code comments or open an issue on GitHub.
