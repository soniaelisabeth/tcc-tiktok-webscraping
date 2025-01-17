# -*- coding: utf-8 -*-
"""TCC DATA TIKTOK.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZSaHTMkab0m7G6VOOk026cbtNTGGCI5l
"""

from wordcloud import WordCloud
import pandas as pd

# Lendo o CSV
data = pd.read_csv('tiktok_data.csv', header=None)

# Definindo as colunas
data.columns = ['id', 'creator', 'hashtags', 'description']

# Limpando as HashTags
data.drop(data[data['hashtags'] == ' '].index, inplace=True)
data

# Limpando hashtags vazias
data.dropna(subset=['hashtags'], inplace=True)

# Concatenando todos os hashtags em uma única string
all_hashtags = ' '.join(data['hashtags'])

# Criando uma nuvem de palavras
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_hashtags)

# Criando uma imagem com a nuvem de palavras com dados crus
image = wordcloud.to_image()

#Separando hashtags numa lista
words_of_hashtags = all_hashtags.split(", ")

excluded_substrings = ['fyp', 'for you', 'foryou', 'foryoupage', 'fypシ', 'fy', 'viral', 'fypシ゚viral']
clean_hashtags = []

for word in words_of_hashtags:
    if not any(substring in word for substring in excluded_substrings):
        clean_hashtags.append(word)

# Criando uma nuvem de palavras
wordcloud = WordCloud(width=1600, height=800, background_color='white', colormap='plasma').generate(' '.join(clean_hashtags))

# Criando uma imagem com a nuvem de palavras com dados limpos
image = wordcloud.to_image()