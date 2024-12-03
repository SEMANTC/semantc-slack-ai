# Slack AI Assistant

A Slack bot that uses Retrieval Augmented Generation (RAG) to answer questions using company documents. The bot integrates with Slack, uses OpenAI's GPT models for generating responses, and Pinecone for vector storage and similarity search.

## Features

- **Document-Grounded Responses**: Uses RAG to provide accurate answers based on company documents
- **Conversation History**: Maintains context through conversation threads
- **Slack Integration**: Seamless integration with Slack workspace
- **Vector Search**: Efficient document retrieval using Pinecone
- **Scalable Architecture**: Built with FastAPI and async support

## Prerequisites

- Python 3.9+
- Slack Workspace Admin access
- OpenAI API key
- Pinecone API key
- Google Cloud Project (for Firestore)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret
SLACK_APP_TOKEN=xapp-your-token

# OpenAI Configuration
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
MAX_TOKENS=2000

# Pinecone Configuration
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=your-environment
PINECONE_INDEX_NAME=your-index

# Google Cloud Settings
PROJECT_ID=your-project
REGION=your-region
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd slack-ai-assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env` file

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
slack-ai-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── conversation.py
│   │   └── vector_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── metadata.py
│   │   └── user.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── context.py
│   │   └── rag_engine.py
│   ├── slack/
│   │   ├── __init__.py
│   │   ├── bot.py
│   │   ├── events.py
│   │   └── handlers/
│   │       ├── __init__.py
│   │       ├── command.py
│   │       └── message.py
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       └── logger.py
├── credentials/
│   └── credentials.json
├── logs/
├── tests/
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

## Usage

### Slack Commands

- `/ask [question]`: Ask a question about company documents
- `/help`: Show help message

### Development

For local development:
1. Install dependencies
2. Set up environment variables
3. Run with hot reload: `uvicorn app.main:app --reload`

### Docker Deployment

Build and run with Docker:

```bash
docker build -t slack-ai-assistant .
docker run -p 8080:8080 slack-ai-assistant
```

## Architecture

- **FastAPI**: Web framework for handling HTTP requests
- **Slack Bolt**: Framework for Slack app development
- **LangChain**: Framework for building LLM applications
- **Pinecone**: Vector database for similarity search
- **Firestore**: Document database for conversation history
- **OpenAI**: LLM provider for generating responses

## Security

- Implements Slack signature verification
- Uses environment variables for sensitive data
- Supports proper access control and user authentication
- Maintains data privacy through secure infrastructure

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
