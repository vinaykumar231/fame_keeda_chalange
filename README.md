# Fame Keeda — Backend Product Builder Challenge

## Overview

This repository contains my implementation for the Fame Keeda Backend Product Builder Challenge for the Backend/API Developer (AI Integration) role. The solution focuses on building scalable backend systems for influencer marketing, with a focus on AI integration and real-time analytics.

## Selected Tracks

I chose to implement the following two sections:

### B. AI Brief Generator

**Why this track?** I wanted to showcase my experience with LLM integrations and function calling. The brief generator demonstrates how AI can streamline campaign creation by automatically generating structured creative briefs based on minimal inputs, with tools for trend research and audience targeting.

![flowchart](https://github.com/user-attachments/assets/fff404ad-fa52-48ac-901a-f1e023ea4e9d)


### 📈 D. Batch ETL & Top-Performer API

**Why this track?** This section demonstrates my ability to build efficient data processing pipelines and expose analytics through a well-designed API. It showcases my skills in handling large datasets and optimizing database queries to deliver valuable insights.

## Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL for persistent storage
- **Cache**: Redis for response caching and performance optimization
- **AI Integration**: Gemini API with function calling
- **ETL**: Custom Python processing with optimized chunking
- **Documentation**: Swagger UI via FastAPI

## Project Structure

```
├── app/
│   ├── __pycache__/
│   ├── .env
│   ├── api/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py 
│   │   │   ├── marketing_campaign.py
│   │   │   └── top_influencers.py
│   │   └── models/
│   │       ├── __pycache__/
│   │       ├── __init__.py
│   │       ├── influencers.py
│   │       ├── marketing_campaign.py
│   │       └── schemas.py
│   ├── .gitignore
│   ├── database.py
│   ├── etl.py
│   ├── llm.py
│   ├── main.py
│   ├── performance.csv
│   ├── prompt.py
│   ├── README.md
│   ├── requirements.txt
│   └── tools.py
```

## Setup & Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- OpenAI API key (for the AI Brief Generator)

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/vinaykumar231/fame_keeda_chalange.git
cd app
```

2. **Set up environment variables**

Create a `.env` file based on the provided `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file and add your configuration values:

```
GOOGLE_API_KEY="your"
SQLALCHEMY_DATABASE_URL = your "

```

3. **Start the services**

This will start:
- The FastAPI application
- PostgreSQL database
- Redis cache

The API will be available at: http://localhost:8000

API documentation can be accessed at: http://localhost:8000/docs

##  API Documentation

![Screenshot 2025-05-07 103359](https://github.com/user-attachments/assets/fae05cd0-ce0f-4f95-acef-7be210ef94a0)

## Performance Considerations

### ETL Performance

- The ETL process is optimized to handle 10k rows in under 2 minutes.
- Chunk processing is implemented to handle large CSV files efficiently.
- Malformed rows are logged and skipped to ensure the process completes successfully.

### API Performance

- Redis caching is implemented for the Brief Generator to provide lightning-fast responses (<100ms) for repeated queries.
- Database queries are optimized with proper indexing on `campaign_id` and `engagement_rate`.
- The Top Performers API is designed to efficiently handle sorting and pagination.

## Trade-offs and Decisions

### AI Brief Generator

1. **OpenAI vs. Open Source LLMs**: I chose OpenAI for production-ready quality, but the code is designed to allow easy swapping with Ollama or HuggingFace models if needed.

2. **Function Calling vs. RAG**: I implemented function calling for tool use rather than RAG. While RAG would allow for more personalized briefs based on historical data, function calling provides a cleaner separation of concerns and is more maintainable.

3. **Redis Caching**: I implemented aggressive caching with a 30-minute TTL to minimize API costs and improve response times, with the understanding that trend data might become slightly stale.

### ETL Pipeline

1. **Batch vs. Stream Processing**: I chose batch processing for simplicity, but the architecture is designed to be extended to stream processing with minimal changes.

2. **In-memory vs. Database Sorting**: For datasets under 100k rows, I perform sorting in memory for better performance. For larger datasets, database-level sorting would be more efficient.

3. **Pandas vs. Custom Processing**: I used Pandas for its optimized CSV handling and aggregation functions, accepting the memory overhead for better development speed and maintainability.

## Future Improvements

Given more time, I would implement the following enhancements:

1. **Add robust authentication and rate limiting**
2. **Implement more sophisticated caching strategies with sliding TTL**
3. **Add comprehensive unit and integration tests**
4. **Implement a streaming version of the metrics pipeline**
5. **Add Grafana dashboards for real-time monitoring**
6. **Deploy the solution to GCP Cloud Run for production readiness**

## Conclusion

This implementation demonstrates how AI can be effectively integrated into influencer marketing workflows, from campaign brief generation to performance analysis. The architecture prioritizes scalability, performance, and developer experience.

## Contact

For any questions about this challenge implementation, please contact me at vinaykumar.pydev@gmail.com
