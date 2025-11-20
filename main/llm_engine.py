import time
import random
import logging
from typing import Generator, Optional
from django.http import StreamingHttpResponse
from langchain_ollama import ChatOllama

# -------------------------------------------------------------------
# 🧠 Model Configuration
# -------------------------------------------------------------------
MODEL_NAME = "llama3.1:8b-instruct-q4_k_m"

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0.7,
    top_p=0.9,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.info(f"✅ Loaded Ollama model: {MODEL_NAME}")


# -------------------------------------------------------------------
# 🧩 Prompt Builder (Reusable for all tools)
# -------------------------------------------------------------------
def build_prompt(system_prompt: str, user_prompt: str) -> str:
    """
    Combine system and user prompts into a structured instruction format.
    """
    return f"""
### SYSTEM
{system_prompt.strip()}

### USER
{user_prompt.strip()}

### ASSISTANT
"""


# -------------------------------------------------------------------
# 🔁 Generic LLM Stream Function
# -------------------------------------------------------------------
def stream_llm_response(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 800,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> StreamingHttpResponse:
    """
    Streams the LLM's response using the given prompts and parameters.
    Can be reused across all tools (quiz gen, lesson planner, summarizer, etc.)
    """
    full_prompt = build_prompt(system_prompt, user_prompt)

    def event_stream() -> Generator[str, None, None]:
        start_time = time.time()
        logging.info("🚀 Starting LLM stream")

        final_response = ""
        try:
            for chunk in llm.stream(full_prompt):
                token = getattr(chunk, "content", None)
                if token:
                    final_response += token
                    yield token
        except Exception as e:
            logging.error(f"⚠️ LLM stream error: {e}")
            yield f"\n⚠️ Error generating response: {e}"
        finally:
            elapsed = time.time() - start_time
            print(final_response)
            logging.info(f"✅ Response completed in {elapsed:.2f}s")

    return StreamingHttpResponse(event_stream(), content_type="text/plain")


# -------------------------------------------------------------------
# 🔄 Utility: Context Reset / Random Seeding
# -------------------------------------------------------------------
def reset_context():
    seed = random.randint(0, 10000)
    random.seed(seed)
    logging.info(f"🔄 Context reset (seed={seed})")
