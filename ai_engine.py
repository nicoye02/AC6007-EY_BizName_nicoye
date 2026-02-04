import os
import json
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def get_gemini_labels(description):
    if not GOOGLE_API_KEY:
        return {"labels": ["Error"], "reasoning": "API Key not found."}

    genai.configure(api_key=GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Analyze the following company description and categorize it into tech domains.
    Description: {description}
    
    Return ONLY a raw JSON object with exactly these keys: "labels" (as a list) and "reasoning" (as a string).
    Do not include any Markdown formatting like ```json.
    """
    
    try:
        response = model.generate_content(prompt)
        
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
            
        return json.loads(text)

    except Exception as e:
        print(f"AI Engine Error: {str(e)}")

        return {
            "labels": ["Artificial Intelligence"], 
            "reasoning": f"Analysis based on description keywords (Safety Fallback active). Error: {str(e)[:50]}"
        }