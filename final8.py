import openpyxl
import pandas as pd
import streamlit as st
import random
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

romantic_df = pd.read_excel('restoran.xlsx')
rock_bar_df = pd.read_excel('Rock_Bar.xlsx')
museum_df = pd.read_excel('müze.xlsx')
spa_df = pd.read_excel('spa.xlsx')
sinema_df = pd.read_excel('sinema.xlsx')
park_df = pd.read_excel('park.xlsx')
lunapark_df = pd.read_excel('lunapark.xlsx')
kareoke_df = pd.read_excel('kareoke.xlsx')
kamp_df = pd.read_excel('kamp.xlsx')
kafe_df = pd.read_excel('kafe.xlsx')
hava_df = pd.read_excel('hava.xlsx')
buz_df = pd.read_excel('buz_pateni.xlsx')
imdb_df = pd.read_csv('imdb.csv')

# romantic_df['aciklama'] = 'restoran'

combined_df = pd.concat([buz_df, kafe_df, romantic_df, rock_bar_df, museum_df, spa_df, sinema_df, park_df, lunapark_df,
                         kareoke_df, kamp_df, hava_df], ignore_index=True)

combined_df["aciklama"] = combined_df["aciklama"].str.strip()

combined_df['tur'] = combined_df['aciklama'].map(
    {'Kafe': 'casual', 'Buz': 'eğlenceli', 'Müze': 'casual', 'Bar': 'eğlenceli', 'Pub': 'eğlenceli',
     'restoran': 'romantik', 'spa': 'romantik', 'sinema': 'eğlenceli', 'Park': 'casual', 'Lunapark': 'eğlenceli',
     'Karaoke': 'eğlenceli', 'kamp': 'eğlenceli', 'Tiyatro': 'eğlenceli'})

combined_df["ad"].isnull().sum()
combined_df["tur"].isnull().sum()
combined_df[['lat', 'long']] = combined_df['location'].str.split(',', expand=True)
combined_df[['lat', 'long']] = combined_df[['lat', 'long']].astype(float)


st.title("_:red[date.py]_")


#st.subheader('Mekan Öneri Uygulaması', divider='rainbow')
#st.subheader('_Streamlit_ is :blue[cool] :sunglasses:')


tur_options = ['casual', 'eğlenceli', 'romantik', 'ev']
selected_tur = st.sidebar.selectbox('Nasıl bir date geçirmek istersiniz?:', tur_options)

if selected_tur == 'ev':

    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import streamlit as st

    pd.set_option('display.max_columns', None)

    df = pd.read_csv('imdb_movies.csv')
    df = df.head(1000)


    features = ['names', 'score', 'genre', 'overview', 'crew', 'date_x']
    for feature in features:
        df[feature] = df[feature].fillna('')

    def combine_features(row):
        return str(row['names']) + ' ' + str(row['score']) + ' ' + str(row['genre']) + ' ' + str(
            row['overview']) + ' ' + str(row['crew']) + ' ' + str(row['date_x'])

    df['combined_features'] = df.apply(combine_features, axis=1)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(count_matrix)

    def get_index_from_title(title):
        title = title.lower()
        return df[df['names'].str.lower() == title].index[0]

    def get_movies_by_actor(actor_name):
        actor_name = actor_name.lower().replace("", "")
        filtered_movies = []
        for index, row in df.iterrows():
            crew_list = row['crew'].lower().replace('', '').split(',')
            if actor_name in crew_list:
                filtered_movies.append(row['names'])
        return filtered_movies

    st.subheader("Partnerinizle ortak beğendiğiniz bir film, oyuncu ya da film türü giriniz. Uygulamamız size en uygun olan filmleri getirecektir.")
    user_input = st.text_input("Bir film adı, bir oyuncu veya bir film türü giriniz:")

    if st.button("Filmleri Öner"):
        try:
            user_input = user_input.lower().strip()

            if user_input in df['crew'].str.lower().str.replace('', '').str.split(',').sum():
                filtered_movies = get_movies_by_actor(user_input)
                if filtered_movies:
                    st.subheader(f":violet[{user_input} isimli oyuncunun oynadığı filmler:]")
                    for movie in filtered_movies:
                        st.write(movie)
                else:
                    st.warning(f"{user_input} isimli oyuncunun oynadığı film bulunamadı.")

            elif user_input.lower() in df['genre'].str.lower().tolist():
                filtered_df = df[df['genre'].str.lower() == user_input.lower()]
                st.subheader(f":violet[{user_input} türündeki filmlerden rastgele seçilenler:]")
                for movie in filtered_df.sample(10)[['names', 'score', 'overview', 'crew', 'date_x']].iterrows():
                    st.write(f"Film Adı: {movie[1]['names']}")
                    st.write(f"Puan: {movie[1]['score']}")
                    st.write(f"Özet: {movie[1]['overview']}")
                    st.write(f"Ekip: {movie[1]['crew']}")
                    st.write(f"Tarih: {movie[1]['date_x']}")
                    st.write("\n")

            else:
                movie_index = get_index_from_title(user_input)
                similar_movies = list(enumerate(cosine_sim[movie_index]))
                sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

                st.subheader(f":violet[{user_input} için benzer filmler:]")
                for i, element in enumerate(sorted_similar_movies[:10]):
                    recommended_movie = df.iloc[element[0]]
                    st.write(f"{i + 1}. Film Adı: {recommended_movie['names']}")
                    st.write(f"Puan: {recommended_movie['score']}")
                    st.write(f"Özet: {recommended_movie['overview']}")
                    st.write(f"Ekip: {recommended_movie['crew']}")
                    st.write(f"Tarih: {recommended_movie['date_x']}")
                    st.write("\n")

        except IndexError:
            st.error("Bu film veritabanında bulunmuyor.")

else:
    butce_options = ['₺', '₺₺', '₺₺₺', '₺₺₺₺']
    selected_butce = st.sidebar.selectbox('Bütçenizi Seçin:', butce_options)


    col1, col2, col3 = st.columns(3)

    if selected_tur == 'casual':
        col1.image('https://i.pinimg.com/564x/c5/0c/49/c50c4934bfb06ba377b1a586ba3455fc.jpg', caption='Casual',
                   use_column_width=True)
    elif selected_tur == 'eğlenceli':
        col1.image('https://i.pinimg.com/564x/bc/8a/09/bc8a09d1f238145c0d05f4593f41e0a8.jpg',
                   caption='Eğlenceli', use_column_width=True)
    else:
        col1.image('https://i.pinimg.com/564x/7b/74/f4/7b74f47a070640872e26b92b04b16b2b.jpg', caption='Romantik',
                   use_column_width=True)

    filtered_df = combined_df[(combined_df['tur'] == selected_tur) & (combined_df['butce'] == selected_butce)]

    if st.sidebar.button("Yeni Öneri Al"):
        filtered_df = combined_df[(combined_df['tur'] == selected_tur) & (combined_df['butce'] == selected_butce)]

    col2.subheader(':white[Önerilen Mekan/Aktivite:]')
    if not filtered_df.empty:
        random_sample = filtered_df.sample(1)
        for index, row in random_sample.iterrows():
            col2.image(row['resim'], caption='Mekan Resmi', use_column_width=True)
            col2.subheader(row['ad'])
            col2.write(f'Puan: {row["puan"]}')
            col2.write(f'Adres: {row["adres"]}')
            col2.write(f'Yorum: {row["yorum"]}')
            col1.write(f' {row["konu"]}')
            col2.write('---')

        col3.subheader(':white[Önerilen Mekanın Konumu:]')
        with col3:
            m = folium.Map(location=[filtered_df['lat'].mean(), filtered_df['long'].mean()], zoom_start=12)

            for index, row in random_sample.iterrows():
                folium.Marker(
                    location=[row['lat'], row['long']],
                    popup=row['ad'],
                    icon=folium.Icon(icon='cloud')
                ).add_to(m)

            folium_static(m)
    else:
        col3.write('Eşleşen mekan bulunamadı.')


