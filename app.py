import pandas as pd
import streamlit as st

#booking color code #003b95
#expedia color code #fddb32
#agoda color code #5a5b5b

#render size
pd.set_option("styler.render.max_elements", 13006180)

# CSV dosyasını yükleyin
uploaded_file = st.file_uploader("Bir CSV dosyası yükleyin", type="csv")

if uploaded_file is not None:
    # CSV dosyasını oku
    df_raw = pd.read_csv(uploaded_file)

    # Her otel için 1, 2 ve 3 kişilik oda fiyatlarının olup olmadığını kontrol edeceğiz
    results = []

    for hotelcode, group in df_raw.groupby('hotelcode'):
        hotel_info = {
            #'hotelcode': hotelcode,
            'hotelname': group['hotelname'].iloc[0],  # Otel ismini alıyoruz
            'B1': "✔️" if not group[(group['WebSiteCode'] == 2) & (group['Guests'] == 1) & (group['OnsiteRate'] > 0)].empty else "❌",
            'B2': "✔️" if not group[(group['WebSiteCode'] == 2) & (group['Guests'] == 2) & (group['OnsiteRate'] > 0)].empty else "❌",
            'B3': "✔️" if not group[(group['WebSiteCode'] == 2) & (group['Guests'] == 3) & (group['OnsiteRate'] > 0)].empty else "❌",
            'E1': "✔️" if not group[(group['WebSiteCode'] == 1) & (group['Guests'] == 1) & (group['OnsiteRate'] > 0)].empty else "❌",
            'E2': "✔️" if not group[(group['WebSiteCode'] == 1) & (group['Guests'] == 2) & (group['OnsiteRate'] > 0)].empty else "❌",
            'E3': "✔️" if not group[(group['WebSiteCode'] == 1) & (group['Guests'] == 3) & (group['OnsiteRate'] > 0)].empty else "❌",
            'A1': "✔️" if not group[(group['WebSiteCode'] == 5) & (group['Guests'] == 1) & (group['OnsiteRate'] > 0)].empty else "❌",
            'A2': "✔️" if not group[(group['WebSiteCode'] == 5) & (group['Guests'] == 2) & (group['OnsiteRate'] > 0)].empty else "❌",
            'A3': "✔️" if not group[(group['WebSiteCode'] == 5) & (group['Guests'] == 3) & (group['OnsiteRate'] > 0)].empty else "❌",
        }
        results.append(hotel_info)

    # Sonuçları bir DataFrame'e dönüştür
    df = pd.DataFrame(results)
    
    # Gerisi aynı kalsın, yani tabloyu filtrele ve renklendir
    st.title("Price Existence with CSV Data")

    # Filtreler tablonun üzerinde olacak şekilde
    st.subheader("Filtreleme Seçenekleri")

    # Otel adı metin girişi ile filtreleme
    filter_name = st.text_input("Otel Adı Giriniz", "")

    # Kişi sayısı filtreleme
    selected_guests = st.multiselect("Kişi Sayısı", options=[1, 2, 3], default=[1, 2, 3])

    # Booking filtreleme
    selected_booking = st.selectbox("Booking Durumu", options=["Tümü", "Fiyat Var", "Fiyat Yok"], index=0)

    # Expedia filtreleme
    selected_expedia = st.selectbox("Expedia Durumu", options=["Tümü", "Fiyat Var", "Fiyat Yok"], index=0)

    # Agoda filtreleme
    selected_agoda = st.selectbox("Agoda Durumu", options=["Tümü", "Fiyat Var", "Fiyat Yok"], index=0)

    # Veri setini filtreleme
    filtered_df = df[df['hotelname'].str.contains(filter_name, case=False, na=False)]

    # Kişi sayısına göre sütunların filtrelenmesi
    if 1 not in selected_guests:
        filtered_df[['B1', 'E1', 'A1']] = ""
    if 2 not in selected_guests:
        filtered_df[['B2', 'E2', 'A2']] = ""
    if 3 not in selected_guests:
        filtered_df[['B3', 'E3', 'A3']] = ""

    # Booking, Expedia ve Agoda filtreleme
    if selected_booking == "Fiyat Var":
        filtered_df = filtered_df[(filtered_df['B1'] == "✔️") | (filtered_df['B2'] == "✔️") | (filtered_df['B3'] == "✔️")]
    if selected_booking == "Fiyat Yok":
        filtered_df = filtered_df[(filtered_df['B1'] == "❌") & (filtered_df['B2'] == "❌") & (filtered_df['B3'] == "❌")]

    if selected_expedia == "Fiyat Var":
        filtered_df = filtered_df[(filtered_df['E1'] == "✔️") | (filtered_df['E2'] == "✔️") | (filtered_df['E3'] == "✔️")]
    if selected_expedia == "Fiyat Yok":
        filtered_df = filtered_df[(filtered_df['E1'] == "❌") & (filtered_df['E2'] == "❌") & (filtered_df['E3'] == "❌")]

    if selected_agoda == "Fiyat Var":
        filtered_df = filtered_df[(filtered_df['A1'] == "✔️") | (filtered_df['A2'] == "✔️") | (filtered_df['A3'] == "✔️")]
    if selected_agoda == "Fiyat Yok":
        filtered_df = filtered_df[(filtered_df['A1'] == "❌") & (filtered_df['A2'] == "❌") & (filtered_df['A3'] == "❌")]

    # Renklendirme fonksiyonları
    def highlight_booking(val):
        color = 'background-color: #003b95'  # Açık mavi renk
        return color

    def highlight_expedia(val):
        color = 'background-color: #fddb32'  # Açık yeşil renk
        return color

    def highlight_agoda(val):
        color = 'background-color: #5a5b5b'  # Açık pembe renk
        return color
        
    # Yeşil renk check işaretleri
    def highlight_check(val):
        return 'color: green' if val == '✔️' else 'color: black'
        
        # Yazıların beyaz olmasını sağlayan stil fonksiyonu
    def make_text_white(val):
        return 'color: white'

    # Renklendirmeleri uygulama
    styled_df = filtered_df.style.applymap(highlight_booking, subset=['B1', 'B2', 'B3']) \
                                 .applymap(highlight_expedia, subset=['E1', 'E2', 'E3']) \
                                 .applymap(highlight_agoda, subset=['A1', 'A2', 'A3']) \
                                 .applymap(highlight_check) \
                                 .applymap(make_text_white)


    # Tablonun tamamını sayfaya sığdırmak için HTML/CSS kullanarak genişlik ayarları yapalım
    st.markdown(
        """
        <style>
        .reportview-container .main .block-container{
            max-width: 100%;
            padding-left: 1%;
            padding-right: 1%;
        }
        table {
            width: 100%;
            table-layout: auto;
            word-wrap: break-word;
            font-size: 10px;  /* Font boyutunu küçülttük */
            border-collapse: collapse;
        }
        th, td {
            text-align: center;
            padding: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Tablonun tarih kısmını üstte göstermek için bir bilgi mesajı
    st.write("Checked for: 2024-09")

    # Filtrelenmiş ve renklendirilmiş tabloyu göster
    st.write(styled_df)



