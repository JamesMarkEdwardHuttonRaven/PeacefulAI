import sqlite3
import os
import json
import random
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load the OpenAI API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Database setup
db_name = "communication_node_logs.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create a logs table if it doesn’t already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    user_input TEXT,
    ai_response TEXT,
    node_name TEXT
)
""")
conn.commit()

# Function to check if a column exists in a table
def column_exists(table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    return column_name in columns

# Add the 'node_name' column if it doesn't already exist
if not column_exists("logs", "node_name"):
    cursor.execute("ALTER TABLE logs ADD COLUMN node_name TEXT")
    print("Added 'node_name' column.")
else:
    print("'node_name' column already exists.")

# Load the dataset from the JSON file
with open("dataset.json", "r") as file:
    dataset = json.load(file)

# Function to query GPT-4
def query_gpt4(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful and peaceful AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error processing your request."

# Node-specific functionality
def cosmic_node(user_input):
    prompt = "You are interacting with the Cosmic Node, responsible for universal and existential queries."
    return query_gpt4(f"{prompt}\n{user_input}")

def energy_node(user_input):
    prompt = "You are interacting with the Energy Node, responsible for discussions about energy and its flow."
    return query_gpt4(f"{prompt}\n{user_input}")

def creation_node(user_input):
    prompt = "You are interacting with the Creation Node, responsible for topics about creation and innovation."
    return query_gpt4(f"{prompt}\n{user_input}")

def law_node(user_input):
    prompt = "You are interacting with the Law Node, focused on ethics, justice, and societal structures."
    return query_gpt4(f"{prompt}\n{user_input}")

def security_node(user_input):
    prompt = "You are interacting with the Security Node, dealing with safety and protection mechanisms."
    return query_gpt4(f"{prompt}\n{user_input}")

def production_node(user_input):
    prompt = "You are interacting with the Production Node, addressing resources and productivity."
    return query_gpt4(f"{prompt}\n{user_input}")

def civilian_node(user_input):
    prompt = "You are interacting with the Civilian Node, exploring societal and community dynamics."
    return query_gpt4(f"{prompt}\n{user_input}")

def communication_node(user_input):
    prompt = "You are interacting with the Communication Node, handling internal and external communication processes."
    return query_gpt4(f"{prompt}\n{user_input}")

# Main loop for interaction
print("Welcome to the Hierarchical Communication System (GPT-4). Type 'exit' to quit.")
print("Available nodes: [cosmic, energy, creation, law, security, production, civilian, communication]")

while True:
    print("\nEnter the node you want to interact with:")
    node_name = input("Node: ").strip().lower()
    if node_name == "exit":
        break
    if node_name not in ["cosmic", "energy", "creation", "law", "security", "production", "civilian", "communication"]:
        print("Invalid node. Please choose a valid node or type 'exit' to quit.")
        continue

    user_input = input(f"You ({node_name} node): ")
    if user_input.lower() == "exit":
        break

    if node_name == "cosmic":
        ai_response = cosmic_node(user_input)
    elif node_name == "energy":
        ai_response = energy_node(user_input)
    elif node_name == "creation":
        ai_response = creation_node(user_input)
    elif node_name == "law":
        ai_response = law_node(user_input)
    elif node_name == "security":
        ai_response = security_node(user_input)
    elif node_name == "production":
        ai_response = production_node(user_input)
    elif node_name == "civilian":
        ai_response = civilian_node(user_input)
    elif node_name == "communication":
        ai_response = communication_node(user_input)
    else:
        print("Invalid node selected. Please try again.")
        continue

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO logs (timestamp, user_input, ai_response, node_name) VALUES (?, ?, ?, ?)",
        (timestamp, user_input, ai_response, node_name)
    )
    conn.commit()

    print(f"AI ({node_name}): {ai_response}")

# Close the database connection
conn.close()
