!pip install -q \ langchain \
langchain-community \ langchain-google-genai \ faiss-cpu \
pypdf \
gradio \
google-generativeai

!pip install sentence-transformers

from langchain_community embeddings import HuggingFaceEmbeddings from langchain_community vectorstores import FAISS
embeddings = HuggingFaceEmbeddings (
model_name="sentence-transformers/all-MiniLM-L6-v2"
db = FAISS. from_documents (docs, embeddings)

!pip install transformers accelerate

from transformers import pipeline
qa_pipeline = pipeline(
"text-generation", model="Qwen/Qwen2-1.5B-Instruct", device_map="auto"
)

def ask(q) :
matched_docs = db. similarity_search (q, k=3)
context = "\n". join([
doc. page_content
for doc in matched_docs
1)
prompt = f"wn
根據以下旅平險條款回答問題。
條款內容：
{context,
問題：
{a}
請用繁體中文回答。
1111
result = qa_pipeline(
prompt, max_new_tokens=200
return result [0] ["generated_text"]

print （ask（"班機延誤可以得到幾元補償？"））
