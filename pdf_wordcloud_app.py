import streamlit as st
from wordcloud import WordCloud
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re

# Ensure NLTK resources are available
def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Preprocess text
def preprocess_text(text):
    # Download resources if not already available
    download_nltk_resources()
    
    # Lowercase the text
    text = text.lower()
    # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\\s]', '', text)
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

# Generate word cloud
def generate_wordcloud(text, max_words=500):
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=max_words).generate(text)
    return wordcloud

# Streamlit app
st.title("📄 PDF WordCloud Generator")

st.header("Upload a PDF File")
pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

if pdf_file is not None:
    # Extract text from PDF
    reader = PdfReader(pdf_file)
    extracted_text = ''
    for page in reader.pages:
        extracted_text += page.extract_text()

    if extracted_text:
        st.subheader("Extracted Text")
        st.write(extracted_text[:500] + "...")  # Show a preview of the text

        # Preprocess the text
        preprocessed_text = preprocess_text(extracted_text)

        # Generate word cloud
        st.subheader("Word Cloud")
        wordcloud = generate_wordcloud(preprocessed_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)
    else:
        st.error("No text could be extracted from the PDF file.")
