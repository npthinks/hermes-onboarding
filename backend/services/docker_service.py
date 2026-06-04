import docker
import os
import subprocess
from services.database import update_user_container, update_user_status, update_pairing_code
#from backend.services.database import update_user_container, update_user_status, update_pairing_code

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_key_here")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_token_here")

def provision_agent(user_id: str):
    try:
        client = docker.from_env()
        
        container = client.containers.run(
            "nousresearch/hermes-agent:latest",
            detach=True,
            name=f"hermes-agent-{user_id}",
            environment={
                "GROQ_API_KEY": GROQ_API_KEY,
                "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
                "USER_ID": user_id,
                "OPENAI_BASE_URL": "https://api.groq.com/openai/v1",
                "OPENAI_API_KEY": GROQ_API_KEY,
                "OPENAI_MODEL": "meta-llama/llama-4-scout-17b-16e-instruct"
            },
            restart_policy={"Name": "unless-stopped"}
        )
        
        update_user_container(user_id, container.id)
        update_user_status(user_id, "ready")
        
        return container.id
        
    except Exception as e:
        update_user_status(user_id, "failed")
        print(f"Failed to provision agent for {user_id}: {str(e)}")
        return None

def stop_agent(user_id: str, container_id: str):
    try:
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        update_user_status(user_id, "stopped")
        return True
    except Exception as e:
        print(f"Failed to stop agent for {user_id}: {str(e)}")
        return False

def get_agent_status(container_id: str):
    try:
        client = docker.from_env()
        container = client.containers.get(container_id)
        return container.status
    except Exception:
        return "not_found"

def get_pairing_code(user_id: str, container_id: str):
    try:
        client = docker.from_env()
        container = client.containers.get(container_id)
        
        result = container.exec_run(
            "hermes pairing list"
        )
        
        output = result.output.decode("utf-8")
        
        for line in output.split("\n"):
            if "pending" in line.lower():
                code = line.split()[-1]
                update_pairing_code(user_id, code)
                return code
                
        return None
        
    except Exception as e:
        print(f"Failed to get pairing code: {str(e)}")
        return None