import os
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from dotenv import load_dotenv

load_dotenv()

# Get the database path relative to Django settings
import django
from django.conf import settings

# Initialize Django if not already initialized
if not settings.configured:
    django.setup()

# Use Django's database configuration
DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')

try:
    # Load database - Use the Django project's SQLite database
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Create SQL Agent
    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=False  # Set to False to avoid verbose output during server operation
    )
except Exception as e:
    print(f"Warning: Could not initialize AI agent: {e}")
    agent = None
