!pip install -q langchain \
langchain-community \ 
langchain-google-genai \ 
faiss-cpu \
pypdf \
gradio \
google-generativeai

from google.colab import files
uploaded = files.upload ()

from langchain_community.document_loaders import TextLoader

loader = TextLoader ("insurance.txt",encoding="utf-8")
documents = loader.load ( )

from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
  chunk_size=500, 
  chunk_overlap=50
)

docs = splitter.split_documents (documents)

!pip install sentence-transformers

from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings (
  model_name="sentence-transformers/all-MiniLM-L6-v2"
）

db = FAISS. from_documents (docs, embeddings)

!pip install transformers accelerate

from transformers import pipeline
qa_pipeline = pipeline(
  "text-generation",
  model="Qwen/Qwen2-1. 5B-Instruct" , 
  device_map="auto"
)

def ask(q):

    # 找出最相關文件
    matched_docs = db.similarity_search(q, k=3)

    # 合併內容
    context = "\n".join([
        doc.page_content
        for doc in matched_docs
    ])

    # Prompt
    prompt = f"""
根據以下旅平險條款回答問題。

條款內容：
{context}

問題：
{q}

請用繁體中文簡短回答。
"""

    # 生成回答
    result = qa_pipeline(
        prompt,
        max_new_tokens=200
    )

    # 只保留新生成內容
    answer = result[0]["generated_text"][len(prompt):]

    return answer.strip()


import gradio as gr

demo = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(
        lines=2,
        placeholder="請輸入保險問題..."
    ),
    outputs="text",
    title="旅平險 AI 問答系統",
    description="上傳保險條款後，可詢問相關問題"
)

demo.launch(share=True)


