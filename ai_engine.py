import os
import json
import google.generativeai as genai
import google.api_core.exceptions

# 环境自适应逻辑
try:
    from google.colab import userdata
    GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
    print("运行环境: Google Colab")
except (ImportError, ModuleNotFoundError):
    # 本地环境读取环境变量
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    print("运行环境: 本地 (Local)")

def get_gemini_labels(description):
    if not GOOGLE_API_KEY:
        return {"labels": ["Error"], "reasoning": "API Key not found."}

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 构建针对 EY 业务逻辑的 Prompt
    prompt = f"""
    Categorize this company: {description}
    Return ONLY a JSON object with EXACTLY these keys: "labels" and "reasoning".
    Example: {{"labels": ["AI"], "reasoning": "Uses ML"}}
    """
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)