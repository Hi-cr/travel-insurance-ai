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
  chunk_size=300, 
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

#驗證程式
test_data = [

    {
        "question": "這份保險的免費申訴電話是多少？",
        "answer": "0800-212-880"
    },

    {
        "question": "本保險契約包含哪些承保項目？",
        "answer": "旅遊傷害保險"
    },

    {
        "question": "保險期間延長最長不得超過幾小時？",
        "answer": "七十二小時"
    },

    {
        "question": "未依約定交付保險費會如何？",
        "answer": "自始不生效力"
    },

    {
        "question": "海外旅行期間從何時開始計算？",
        "answer": "完成出境手續"
    },

    {
        "question": "重大燒燙傷保險的給付項目是什麼？",
        "answer": "重大燒燙傷保險金"
    },

    {
        "question": "保險契約解釋有疑義時應如何處理？",
        "answer": "有利於被保險人的解釋"
    }

]

correct = 0

for item in test_data:

    pred = ask(item["question"])

    print("問題：", item["question"])
    print("AI回答：", pred)
    print("標準答案：", item["answer"])

    if item["answer"] in pred:
        print("結果：正確\n")
        correct += 1
    else:
        print("結果：錯誤\n")

accuracy = correct / len(test_data)

print("Accuracy:", accuracy)




