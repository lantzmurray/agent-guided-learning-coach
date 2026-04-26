import requests
import json
from tinydb import TinyDB, Query
from typing import Dict, Any, List
from datetime import datetime
import logging


# Configure logging for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



"""
Base Agent - Shared functionality for all AthenaCore agents
For AthenaCore multi-agent collaboration system
"""

# Initialize TinyDB for persistent shared memory
db = TinyDB("memory/memory_store.json")
Topic = Query()
OLLAMA_TIMEOUT_SECONDS = 1800

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def _read_ollama_stream(response: requests.Response) -> str:
    """Read Ollama's streamed NDJSON chunks into one response string."""
    chunks = []
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        data = json.loads(line)
        chunks.append(data.get("response", ""))
        if data.get("done"):
            break
    return "".join(chunks).strip()


def call_llm(prompt: str, model: str = "llama2") -> str:
    """
    Call Ollama API for LLM inference
    
    Args:
        prompt: Prompt to send to LLM
        model: LLM model to use (default: llama2)
    
    Returns:
        LLM response string
    """
    try:
        with requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True,
            },
            timeout=(10, OLLAMA_TIMEOUT_SECONDS),
            stream=True,
        ) as response:
            response.raise_for_status()
            return _read_ollama_stream(response)
    except requests.RequestException as e:
        return f"Error calling LLM: {str(e)}"


def log_agent_response(topic: str, agent: str, content: str) -> None:
    """
    Log agent response to shared memory
    
    Args:
        topic: Research topic
        agent: Agent name (e.g., "Research Agent")
        content: Agent's response/content
    """
    timestamp = datetime.now().isoformat()
    
    if db.contains(Topic.name == topic):
        # Update existing topic
        db.update(
            lambda t: t["log"].append({
                "agent": agent,
                "content": content,
                "timestamp": timestamp
            }),
            Topic.name == topic
        )
    else:
        # Create new topic
        db.insert({
            "name": topic,
            "log": [{
                "agent": agent,
                "content": content,
                "timestamp": timestamp
            }],
            "created_at": timestamp
        })


def get_topic_log(topic: str) -> List[Dict[str, Any]]:
    """
    Retrieve complete log for a topic
    
    Args:
        topic: Topic name
    
    Returns:
        List of log entries (agent, content, timestamp)
    """
    result = db.search(Topic.name == topic)
    if result:
        return result[0]["log"]
    return []


def get_all_topics() -> List[str]:
    """
    Get list of all topics in shared memory
    
    Returns:
        List of topic names
    """
    return [item["name"] for item in db.all()]


def delete_topic(topic: str) -> bool:
    """
    Delete a topic and all its log entries
    
    Args:
        topic: Topic name to delete
    
    Returns:
        True if deleted, False if not found
    """
    if db.contains(Topic.name == topic):
        db.remove(Topic.name == topic)
        return True
    return False


def get_agent_contributions(topic: str, agent: str) -> List[Dict[str, Any]]:
    """
    Get all contributions from a specific agent on a topic
    
    Args:
        topic: Topic name
        agent: Agent name
    
    Returns:
        List of agent's contributions
    """
    log = get_topic_log(topic)
    return [entry for entry in log if entry["agent"] == agent]


def get_topic_summary(topic: str) -> Dict[str, Any]:
    """
    Get summary statistics for a topic
    
    Args:
        topic: Topic name
    
    Returns:
        Dictionary with summary statistics
    """
    log = get_topic_log(topic)
    
    if not log:
        return {
            "topic": topic,
            "total_entries": 0,
            "agents": [],
            "first_entry": None,
            "last_entry": None
        }
    
    # Get unique agents
    agents = list(set(entry["agent"] for entry in log))
    
    return {
        "topic": topic,
        "total_entries": len(log),
        "agents": agents,
        "first_entry": log[0]["timestamp"],
        "last_entry": log[-1]["timestamp"],
        "log": log
    }
