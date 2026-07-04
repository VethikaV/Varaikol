import requests
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL

def call_llm(prompt: str, system: str = "You are a helpful drawing assistant.") -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "AI Drawing Assistant"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(OPENROUTER_BASE_URL, json=body, headers=headers)
    res.raise_for_status()
    
    data = res.json()
    
    # Debug: print full response to terminal so you can see what's coming back
    print("OpenRouter response:", data)
    
    content = data["choices"][0]["message"]["content"]
    
    # Ensure it's always a string
    if content is None:
        return ""
    return str(content)