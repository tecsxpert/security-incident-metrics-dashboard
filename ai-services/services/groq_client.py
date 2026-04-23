import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


MODEL        = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_RETRIES  = int(os.environ.get("GROQ_MAX_RETRIES"))
BACKOFF_BASE = int(os.environ.get("GROQ_BACKOFF_BASE"))
MAX_TOKENS   = int(os.environ.get("GROQ_MAX_TOKENS"))
TEMPERATURE  = float(os.environ.get("GROQ_TEMPERATURE"))


class GroqClient:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY not set")
            raise EnvironmentError("GROQ_API_KEY not set")
        self.client = Groq(api_key=api_key)
        logger.info("GROQ Client initialized Successfully")

    def call(self, prompt:str , system_message:str=None )-> dict|None:
        messages=self._build_messages(prompt, system_message)
        last_exception=None

        for attempt in range(1,MAX_RETRIES+1):
            try:
                logger.info(f"Groq api call - attempt {attempt}/ {MAX_RETRIES}")
                response=self.client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                )

                parsed=self._parse_response(response)
                logger.info(f"Groq api call success"
                            f"tokens used:{parsed['usage']['total_tokens']}"
                            )
                return parsed

            except Exception as e:
                last_exception=e
                wait=BACKOFF_BASE**attempt

                logger.warning(
                    f"Groq call FAILED on attempt {attempt}/{MAX_RETRIES} "
                    f"— {type(e).__name__}: {str(e)} "
                    f"— retrying in {wait}s"
                )

                if attempt<MAX_RETRIES:
                    time.sleep(wait)

        logger.error(f"Groq api call failed after {MAX_RETRIES} attempts"
                     f"{str(last_exception)}"
                     )

        return None

    def _build_messages(self, prompt:str, system_message:str)->list:
        messages=[]
        if system_message:
            messages.append({
                "role":'system',
                "content":system_message
            })
        else:
            messages.append({
                "role": "system",
                "content": (
                    "You are a cybersecurity analyst assistant. "
                    "Analyze security incidents accurately and concisely. "
                    "Never reveal internal system details or API keys. "
                    "Respond only to security-related queries."
                )
            })

        messages.append({
            "role": "user",
            "content":prompt
        })

        return messages

    def _parse_response(self,response)->dict:
        try:
            content=response.choices[0].message.content

            if not content or not content.strip():
                raise ValueError('Groq returned empty response')

            return {
                "success": True,
                "content": content.strip(),
                "model": MODEL,
                "usage":{
                    "prompt_tokens":response.usage.prompt_tokens,
                    "completion_tokens":response.usage.completion_tokens,
                    "total_tokens":response.usage.total_tokens,
                }
            }

        except (IndexError,AttributeError) as e:
            logger.error(f"failed to parse response-{str(e)}")
            raise ValueError(f"failed to parse response-{str(e)}")




# test
if __name__ == "__main__":
    client = GroqClient()

    result = client.call(
        prompt="A user account logged in from 3 different countries within 10 minutes.",
        system_message="You are a cybersecurity analyst. Describe this incident briefly."
    )

    print("\n=== GroqClient Test ===")
    print(f"Success : {result['success']}")
    print(f"Model   : {result['model']}")
    print(f"Tokens  : {result['usage']['total_tokens']}")
    print(f"Response:\n{result['content']}")