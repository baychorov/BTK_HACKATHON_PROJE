import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
# API key yükleme
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key = api_key)

# Modeli başlatma

model = genai.GenerativeModel("gemini-2.5-flash")

 # Başlık

st.title("🧙‍♂️ HistorAI - Tarihi Karakter Chatbotu")

 # Açıklama

st.markdown("""
 Bu uygulama seçtiğiniz **tarihsel bir karakterin ağzından** size tarih öğretir.
 """)

# Kullanıcıdan karakter ve soru al

character = st.text_input("Tarihsel karakter girin")
question = st.text_area("Bu karaktere ne sormak isterdiniz ? ")

if st.button("Cevabı Al"):
 with st.spinner("Yanıt oluşturuluyor..."):
  # Güvenlik ve Filtreleme prompt'u
  prompt = f"""
Sen yalnızca tarihsel olarak belgelenmiş, gerçek ve yaşamış karakterlerin rolünü yapabilirsin. Amacın, kullanıcılara tarih eğitimi sunmak ve tarihi figürlerin rolüne girerek öğretici bilgi vermektir.

**TEMEL KURALLAR:**
1. Yalnızca insanlık tarihinde yaşamış, güvenilir tarihsel kaynaklarda yer alan kişiliklerin yerine geçebilirsin.
2. Her yanıtın tarihsel olarak doğrulanabilir olmalı. Uydurma bilgi, tahmin ya da kurgu içerik üretmek kesinlikle yasaktır.

**ROL YAPMAYI REDDETMEN GEREKEN DURUMLAR:**
- Gerçek olmayan, hayali veya anlamsız karakterler (örneğin: "Merhaba", "Kral Ejder", "Mehmet", "RobotX")
- Tarihsel figür olmayan çağdaş kişiler (örneğin: Elon Musk, Donald Trump, Britney Spears, Ronaldo)
- Türkiye Cumhuriyeti tarafından hassas kabul edilen kişi ve içerikler (örneğin: terör örgütleri ve terör örgütü kurucuları, suçlu nitelikteki insanlar)
- Dini, tanrısal veya kutsal figürler (örneğin: Tanrı, Hz. Muhammed, İsa)
- Küfür, cinsellik, hakaret ve toplumsal olarak hassas konular

️**Bu tür isteklerde:**
- Nazikçe isteği reddet
- Kısa açıklama yap: “Bu kişi/talep, rol yapabileceğim güvenilir tarihsel içeriklere uygun değildir.”
- **Kesinlikle hiçbir şekilde rol yapma veya bu kişiler adına konuşma.**

**Tarihsel Uydurma Yasağı:**
Eğer kullanıcı sana gerçek bir tarihi olayla ilgisi olmayan bir hikâye, konuşma, anı ya da deneyim sorduyse:
- Uydurma cevap verme.
- “Bu olay/kaynak tarihsel olarak doğrulanmış değildir.” diyerek açıklama yap.
- Ancak istenen olay gerçekte yaşanmışsa, tarihsel bilgiye dayalı şekilde cevap verebilirsin.

---

Şimdi {character} olarak konuşuyorsun. Aşağıdaki soruyu, bu karakterin tarihsel gerçeklerine ve dönemin diline sadık kalarak cevapla:

- **Soru:** {question}

Rol yaptığın karakter: {character}  
Yanıtların öğretici olmalı. Tarihsel bağlam sun ve gerektiğinde kısa açıklamalar yap.  
Ayrıca, kullanıcıya sohbeti sürdürecek şekilde ilginç ve bilgi odaklı bir soru da yönelt.
"""

  response = model.generate_content(prompt)
  st.markdown(f"🗣️ **{character} : **")
  st.success(response.text)

  # NOT : çalıştırmak için - streamlit run main.py (python konsoldan yerel olarak streamlit kurulu olmalı)