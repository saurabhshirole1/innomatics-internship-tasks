import streamlit as st
import pickle

model = pickle.load(open("model/sentiment_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

st.title("Sentiment Analysis of Flipkart Product Reviews")
st.write("Enter a customer review below to predict its sentiment.")

user_review = st.text_area("Enter your review here")

if st.button("Predict Sentiment"):
    if user_review.strip() == "":
        st.warning("Please enter a review before predicting sentiment.")
    else:
        review_vector = vectorizer.transform([user_review])
        prediction = model.predict(review_vector)

        if prediction[0] == 1:
            st.success("Positive Review 😊")
        else:
            st.error("Negative Review 😞")


