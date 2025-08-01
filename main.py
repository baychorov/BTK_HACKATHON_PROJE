import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# API key yükleme
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Modeli başlatma
model = genai.GenerativeModel("gemini-2.5-flash")

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="HistorAI - Tarihi Karakter Chatbotu",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Stilleri
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

    /* Ana container */
    .main-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border: 2px solid #d4af37;
    }

    /* Başlık stilleri */
    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #d4af37, #ffd700, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
        letter-spacing: 2px;
    }

    .subtitle {
        font-family: 'Crimson Text', serif;
        font-size: 1.3rem;
        text-align: center;
        color: #e8e8e8;
        font-style: italic;
        margin-bottom: 2rem;
        opacity: 0.9;
    }

    /* Kart tasarımı */
    .historic-card {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 
            inset 5px 5px 10px rgba(0,0,0,0.3),
            inset -5px -5px 10px rgba(255,255,255,0.1),
            0 10px 20px rgba(0,0,0,0.2);
        border: 1px solid #d4af37;
        margin: 1.5rem 0;
    }

    /* Input stilleri */
    .stTextInput > div > div > input {
        background: linear-gradient(145deg, #34495e, #2c3e50) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 10px !important;
        color: #ecf0f1 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1.1rem !important;
        padding: 0.75rem !important;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 0.2rem rgba(212, 175, 55, 0.25), inset 2px 2px 5px rgba(0,0,0,0.3) !important;
    }

    .stTextArea > div > div > textarea {
        background: linear-gradient(145deg, #34495e, #2c3e50) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 10px !important;
        color: #ecf0f1 !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1.1rem !important;
        padding: 0.75rem !important;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.3) !important;
    }

    /* Buton stilleri */
    .stButton > button {
        background: linear-gradient(45deg, #d4af37, #b8860b) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3) !important;
        text-transform: uppercase !important;
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, #ffd700, #d4af37) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4) !important;
    }

    /* Yanıt alanı */
    .response-container {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #d4af37;
        box-shadow: 
            0 10px 30px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        margin: 2rem 0;
    }

    .character-name {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #d4af37;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .response-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #ecf0f1;
        text-align: justify;
        text-indent: 2rem;
    }

    /* Dekoratif elementler */
    .ornament {
        text-align: center;
        font-size: 2rem;
        color: #d4af37;
        margin: 2rem 0;
        opacity: 0.7;
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e, #16213e) !important;
    }

    /* Spinner özelleştirme */
    .stSpinner > div {
        border-top-color: #d4af37 !important;
    }

    /* Başarı mesajı */
    .stSuccess {
        background: linear-gradient(145deg, #27ae60, #2ecc71) !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Crimson Text', serif !important;
    }

    /* Label stilleri */
    .stTextInput > label, .stTextArea > label {
        font-family: 'Cinzel', serif !important;
        color: #d4af37 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Ana sayfa arkaplanı */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 75%, #0f3460 100%);
    }

    /* Tarihi karakter önerileri */
    .suggestions-container {
        background: linear-gradient(145deg, #2c3e50, #34495e);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #d4af37;
        margin: 1rem 0;
    }

    .suggestion-chip {
        display: inline-block;
        background: linear-gradient(45deg, #d4af37, #b8860b);
        color: #1a1a2e;
        padding: 0.4rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-family: 'Crimson Text', serif;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .suggestion-chip:hover {
        background: linear-gradient(45deg, #ffd700, #d4af37);
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Ana sayfa başlığı
st.markdown("""
<div class="main-container">
    <h1 class="main-title">🏛️ HistorAI</h1>
    <p class="subtitle">Tarihi Karakterlerle Sohbet Edin ve Geçmişi Keşfedin</p>
    <div class="ornament">⚜️ ◆ ⚜️</div>
</div>
""", unsafe_allow_html=True)

# Açıklama bölümü
st.markdown("""
<div class="historic-card">
    <h3 style="color: #d4af37; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1rem;">
        🧙‍♂️ Tarihle Buluşun
    </h3>
    <p style="color: #ecf0f1; font-family: 'Crimson Text', serif; font-size: 1.1rem; text-align: center; line-height: 1.6;">
        Bu uygulama seçtiğiniz <strong style="color: #d4af37;">tarihsel bir karakterin ağzından</strong> size tarih öğretir.<br>
        Geçmişin büyük isimlerini canlandırarak, tarihi kendi dillerinden dinleyin.
    </p>
</div>
""", unsafe_allow_html=True)

# İki sütunlu layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="historic-card">
        <h4 style="color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 1rem;">
            👤 Tarihi Karakter Seçin
        </h4>
    </div>
    """, unsafe_allow_html=True)

    character = st.text_input(
        "Hangi tarihi karakterle konuşmak istersiniz?",
        placeholder="Örn: Napoleon Bonaparte, Fatih Sultan Mehmet, Leonardo da Vinci..."
    )

    # Karakter önerileri
    st.markdown("""
    <div class="suggestions-container">
        <h5 style="color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 0.8rem;">
            💡 Popüler Seçimler:
        </h5>
        <span class="suggestion-chip">Napoleon Bonaparte</span>
        <span class="suggestion-chip">Fatih Sultan Mehmet</span>
        <span class="suggestion-chip">Leonardo da Vinci</span>
        <span class="suggestion-chip">Mimar Sinan</span>
        <span class="suggestion-chip">Kleopatra</span>
        <span class="suggestion-chip">Yunus Emre</span>
        <span class="suggestion-chip">İbn-i Sina</span>
        <span class="suggestion-chip">Piri Reis</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="historic-card">
        <h4 style="color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 1rem;">
            💬 Sorunuzu Yöneltin
        </h4>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "Bu karaktere ne sormak isterdiniz?",
        placeholder="Örn: En büyük başarınız neydi? O dönemde yaşam nasıldı? Hangi zorluklarla karşılaştınız?",
        height=150
    )

# Ortalanmış buton
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    if st.button("🔮 Cevabı Al", use_container_width=True):
        if character and question:
            with st.spinner("📜 Tarihsel bilgiler araştırılıyor..."):
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
- Kısa açıklama yap: "Bu kişi/talep, rol yapabileceğim güvenilir tarihsel içeriklere uygun değildir."
- **Kesinlikle hiçbir şekilde rol yapma veya bu kişiler adına konuşma.**

**Tarihsel Uydurma Yasağı:**
Eğer kullanıcı sana gerçek bir tarihi olayla ilgisi olmayan bir hikâye, konuşma, anı ya da deneyim sorduysa:
- Uydurma cevap verme.
- "Bu olay/kaynak tarihsel olarak doğrulanmış değildir." diyerek açıklama yap.
- Ancak istenen olay gerçekte yaşanmışsa, tarihsel bilgiye dayalı şekilde cevap verebilirsin.

---

Şimdi {character} olarak konuşuyorsun. Aşağıdaki soruyu, bu karakterin tarihsel gerçeklerine ve dönemin diline sadık kalarak cevapla:

- **Soru:** {question}

Rol yaptığın karakter: {character}  
Yanıtların öğretici olmalı. Tarihsel bağlam sun ve gerektiğinde kısa açıklamalar yap.  
Ayrıca, kullanıcıya sohbeti sürdürecek şekilde ilginç ve bilgi odaklı bir soru da yönelt.
"""

                try:
                    response = model.generate_content(prompt)

                    # Yanıt gösterimi
                    st.markdown("""
                    <div class="response-container">
                        <div class="character-name">
                            🗣️ <strong>{}</strong> yanıtlıyor:
                        </div>
                        <div class="response-text">
                            {}
                        </div>
                    </div>
                    """.format(character, response.text), unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"⚠️ Bir hata oluştu: {str(e)}")
        else:
            st.warning("⚠️ Lütfen hem tarihi karakter hem de soru alanını doldurun!")

# Alt bilgi
st.markdown("""
<div class="ornament">⚜️ ◆ ⚜️</div>
<div style="text-align: center; color: #7f8c8d; font-family: 'Crimson Text', serif; margin-top: 3rem;">
    <p>📚 <em>Tarihi kişiliklerle etkileşime geçerek geçmişi keşfedin</em></p>
    <p style="font-size: 0.9rem; opacity: 0.7;">
        Bu uygulama eğitim amaçlıdır ve tarihsel bilgilere dayanır
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar bilgileri
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(145deg, #2c3e50, #34495e); padding: 1.5rem; border-radius: 12px; border: 1px solid #d4af37; margin-bottom: 1rem;">
        <h3 style="color: #d4af37; font-family: 'Cinzel', serif; text-align: center;">
            📖 Nasıl Kullanılır?
        </h3>
        <ol style="color: #ecf0f1; font-family: 'Crimson Text', serif; line-height: 1.6;">
            <li>Konuşmak istediğiniz tarihi karakteri yazın</li>
            <li>Bu karaktere yöneltmek istediğiniz soruyu girin</li>
            <li>"Cevabı Al" butonuna tıklayın</li>
            <li>Tarihi karakter sizinle kendi diliyle konuşacak!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(145deg, #2c3e50, #34495e); padding: 1.5rem; border-radius: 12px; border: 1px solid #d4af37;">
        <h3 style="color: #d4af37; font-family: 'Cinzel', serif; text-align: center;">
            💡 İpuçları
        </h3>
        <ul style="color: #ecf0f1; font-family: 'Crimson Text', serif; line-height: 1.6;">
            <li>Detaylı sorular sorun</li>
            <li>Dönemin yaşam tarzını merak edin</li>
            <li>Kişisel deneyimlerini öğrenin</li>
            <li>Tarihi olaylar hakkında bilgi alın</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

