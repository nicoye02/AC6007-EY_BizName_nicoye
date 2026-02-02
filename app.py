from flask import Flask, render_template, request, jsonify
import pandas as pd
import openai  # 用于调用大模型解决词义理解问题
from scraper import get_business_description  # 自定义抓取模块

app = Flask(__name__)

# 定义 EY 要求的技术领域 
TECH_DOMAINS = [
    "Communications & connectivity", "Privacy & security", 
    "Blockchain", "Digital content management", 
    "Artificial intelligence", "Human-machine collaboration system", 
    "Cloud & quantum computing"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    company_name = request.form.get('company_name')
    # 1. 抓取原始数据（解决表格和描述提取问题）
    raw_desc, table_data = get_business_description(company_name)
    
    # 2. 使用 AI 进行语义标注（解决“无法理解词义”痛点 [cite: 1, 3]）
    labels = ai_semantic_labeling(raw_desc)
    
    return jsonify({
        "description": raw_desc,
        "labels": labels,
        "tables": table_data
    })

def ai_semantic_labeling(description):
    """
    使用 AI 进行互斥且完备的分类 [cite: 18, 20]
    """
    prompt = f"分析以下业务描述，从{TECH_DOMAINS}中选出最匹配的标签：{description}"
    # 这里调用 OpenAI API
    # response = openai.ChatCompletion.create(...)
    return "Artificial intelligence" # 示例返回

if __name__ == '__main__':
    app.run(debug=True)
