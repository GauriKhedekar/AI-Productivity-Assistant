import requests


def generate_daily_summary(input_text: str) -> str:
    """
    Generates daily productivity summary using local Ollama model.
    Make sure Ollama is running.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": input_text,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": 350,
                    "top_p": 0.9
                }
            },
            timeout=120
        )

        response.raise_for_status()
        return response.json()["response"].strip()

    except Exception as e:
        return f"Ollama error: {str(e)}"
