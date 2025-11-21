import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

async def get_gemini_response(
    message: str, 
    api_key: str = None, 
    model: str = "gemini-1.5-flash", 
    history: list = [], 
    context: str = "",
    system_instruction: str = None
):
    active_key = api_key or GEMINI_API_KEY
    if not active_key:
        return "Error: Gemini API Key not configured"
        
    genai.configure(api_key=active_key)
    
    # Normalize model name - remove 'models/' prefix if present
    # Gemini SDK expects just the model name, not the full path
    normalized_model = model.replace("models/", "") if model else "gemini-1.5-flash"
    
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
    
    # Convert history to Gemini format if needed, or just append to prompt
    # Gemini API supports history in start_chat, but for simplicity/statelessness we can append to prompt
    # or use start_chat with history.
    
    # Let's use the chat session object if possible, but here we just have a list of dicts
    # history format: [{'role': 'user', 'parts': ['msg']}, {'role': 'model', 'parts': ['msg']}]
    
    # Map 'assistant' to 'model' for Gemini
    formatted_history = []
    for msg in history:
        role = 'model' if msg['role'] == 'assistant' else 'user'
        formatted_history.append({'role': role, 'parts': msg['parts']})
        
    chat = gemini_model.start_chat(history=formatted_history)
    
    # Send message with system prompt context (as a user message first? or just prepend?)
    # A common trick is to prepend context to the latest message or use a system instruction if supported.
    # Gemini 1.5 Flash supports system_instruction in model init, but we are re-initing.
    
    # Let's try prepending context to the message for now, it's robust.
    full_message = f"{system_prompt}\n\nUser Question: {message}"
    
    try:
        response = chat.send_message(full_message)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"
