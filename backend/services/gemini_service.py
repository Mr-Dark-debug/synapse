import os
import asyncio
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fastapi import HTTPException

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Timeout constant
GEMINI_TIMEOUT_SECONDS = 30


async def _generate_response_internal(
    chat,
    full_message: str
) -> str:
    """Internal function to generate response from Gemini."""
    try:
        response = await asyncio.to_thread(chat.send_message, full_message)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True
)
async def _get_gemini_response_with_retry(
    chat,
    full_message: str
) -> str:
    """Wrapper with retry logic for transient failures."""
    try:
        # Apply timeout to the entire operation
        response_text = await asyncio.wait_for(
            _generate_response_internal(chat, full_message),
            timeout=GEMINI_TIMEOUT_SECONDS
        )
        return response_text
    except asyncio.TimeoutError as e:
        logger.error(f"Gemini request timed out after {GEMINI_TIMEOUT_SECONDS}s")
        raise HTTPException(
            status_code=504,
            detail=f"AI request timed out after {GEMINI_TIMEOUT_SECONDS} seconds. Please try a shorter query."
        )
    except Exception as e:
        logger.error(f"Error in Gemini response generation: {str(e)}")
        raise


async def get_gemini_response(
    message: str, 
    api_key: str = None, 
    model: str = "gemini-1.5-flash", 
    history: list = [], 
    context: str = "",
    system_instruction: str = None
) -> str:
    """
    Get response from Gemini AI with timeout and retry logic.
    
    Args:
        message: User message/query
        api_key: Gemini API key (uses env var if not provided)
        model: Model name (e.g., "gemini-1.5-flash")
        history: Chat history in format [{'role': 'user'/'assistant', 'parts': [...]}]
        context: Additional context (e.g., paper contents)
        system_instruction: Custom system instruction
        
    Returns:
        AI response text
        
    Raises:
        HTTPException: For various error conditions (400, 504, 500)
    """
    # Validate API key
    active_key = api_key or GEMINI_API_KEY
    if not active_key:
        logger.error("No Gemini API key configured")
        raise HTTPException(
            status_code=400,
            detail="Gemini API key not configured. Please add it in Settings."
        )
        
    try:
        # Configure with the active key
        genai.configure(api_key=active_key)
        
        # Normalize model name - remove 'models/' prefix if present
        normalized_model = model.replace("models/", "") if model else "gemini-1.5-flash"
        
        logger.info(f"Generating response with model: {normalized_model}")
        
        # Create model instance
        gemini_model = genai.GenerativeModel(normalized_model)
        
        # Construct system prompt with context
        base_prompt = """
        You are a research assistant helping a user understand scientific papers.
        """
        
        if system_instruction:
            base_prompt = system_instruction

        system_prompt = f"""
        {base_prompt}
        
        Context from selected papers:
        {context}
        
        Instructions:
        1. Answer based on the context provided.
        2. If the answer is not in the context, use your general knowledge but mention that it's not in the papers.
        3. Be concise and helpful.
        """
        
        # Format history - map 'assistant' to 'model' for Gemini
        formatted_history = []
        for msg in history:
            role = 'model' if msg['role'] == 'assistant' else 'user'
            formatted_history.append({'role': role, 'parts': msg['parts']})
            
        # Start chat session with history
        chat = gemini_model.start_chat(history=formatted_history)
        
        # Prepare full message with context
        full_message = f"{system_prompt}\n\nUser Question: {message}"
        
        # Get response with retry and timeout
        response_text = await _get_gemini_response_with_retry(chat, full_message)
        
        logger.info("Successfully generated response")
        return response_text
        
    except HTTPException:
        # Re-raise HTTP exceptions (already formatted)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_gemini_response: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI response: {str(e)}"
        )

