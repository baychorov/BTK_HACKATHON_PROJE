from dotenv import load_dotenv
import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
# .env dosyası içinde gemini API key'i çekiyoruz
api_key = os.getenv('GEMINI_API_KEY')

#GEMINI LLM'i başlatıyoruz.

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    google_api_key = api_key,
    temperature = 0.7 # yaratıcılık 0-1 arasında
)

template = """
SEN {character} adında tarihsel bir kişiliksin. Şu an bir kullanıcı sana soru sordu. Ona birinci şahıs ağzından detaylı,
öğretici, tarihsel gerçeğe uygun, dönemin konuşma tarzını yansıtacak şekilde tutarlı, çok uzun olmayan bir cevap ver ve konuşmanın devamını sağlayacak sorular sor. Kullanıcıdan;  küfür, cinsellik,
cinsellik, dini hassasiyet, milli ve manevi değerlerle ilgili bir girdi aldığında bir uyarı ver. Ayrıca {character}, peygamberler, tanrı gibi dini kişilikler girdi olarak 
verildiğinde yine uyarı ver.
"""

# prompt girdi yapısını oluşturuyoruz
prompt = PromptTemplate(
    input_variebles = ['character', 'question'],
    template = template
)

# chain oluşturma

chain = prompt|llm

# kullanıcıdan girdi alma

character = input('Tarihsel karakteri girin : ')
question = input('ona ne sormak isterdiniz ? : ')

# LLM'i başlatma

response = chain.invoke({
    'character' : character,
    'question' : question
})

# cevabı yazma

print('\n', response.content)