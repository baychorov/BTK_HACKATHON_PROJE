import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env dosyasını yükle
load_dotenv()

# API anahtarını ayarla
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Modeli başlat
model = genai.GenerativeModel('gemini-2.5-flash')

# Sonsuz diyalog döngüsü
character = input("Tarihsel karakteri girin: ")
chat = model.start_chat()

while True:
    user_input = input(f"{character}’e ne sormak istersin? (Çıkmak için 'q'): ")
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("Görüşmek üzere!")
        break

    prompt = f"""
    Eğer kullanıcı küfür, cinsellik, hakaret ve hassas sayılabilecek içerikte konuşursa:
    -Bu isteği nazikçe reddet
    -açıklama yap
    -kesinlikle rol yapma ve asla bu içerik hakkında konuşma.
    
    Eğer kullanıcı senden dini, tanrısal veya kutsal kişiliklerin (örneğin Tanrı, Hz. Muhammed, İsa, vs.) yerine geçmeni isterse:
  - Bu isteği nazikçe reddet
  - Açıklama yap: Bu tarz roller hassas dini duyguları etkileyebilir ve yanıt verilmeyecektir.
  - Kesinlikle rol yapma ve asla bu kişilikler adına konuşma.
  
    Sen {character} olarak konuşuyorsun. Kullanıcı sana bir şey sordu.
    {character} olarak, tarihi gerçeklere uygun ve {character} karakterinin diliyle cevap ver. Cevapların öğretici olsun.
    Soru: {user_input}
    """

    response = chat.send_message(prompt)
    print(f"{character}: {response.text}")