import streamlit as st
import requests

# Define the pages
PAGES = {
    "Home": "Welcome to the Sentiment Analysis Web App!",
    "About": (
        "This web app performs sentiment analysis specifically on tweets to determine their emotional tone.\n\n"
        "### How It Works\n"
        "When you enter a tweet and submit it, the app sends the tweet to a machine learning model that has been trained "
        "on a large dataset of tweets. The model analyzes the text and returns a sentiment prediction.\n\n"
        "### Sentiment Categories\n"
        "The sentiment analysis model classifies the tweet into one of the following categories:\n\n"
        "0 - **Neutral**: The tweet does not convey a strong emotional tone. It is neither positive nor negative.\n"
        "1 - **Negative**: The tweet conveys negative sentiment, expressing dislike, anger, or hostility towards the subject or entity.\n"
        "2 - **Positive**: The tweet conveys positive sentiment, expressing affection, admiration, or enjoyment towards the subject or entity.\n\n"
        "### Example Predictions\n"
        "- **Neutral**: \"Just had a normal day at work.\"\n"
        "- **Negative**: \"I can’t believe how terrible this experience was!\"\n"
        
        "- **Positive**: \"Absolutely loving this new gadget!\"\n\n"
        "Feel free to enter your own tweet to see how it is classified by the model. The model is designed to handle the "
        "informal language and short length typical of tweets."
    ),
    "Prediction": "Enter a tweet to get a sentiment analysis."
}

def main():
    # Sidebar for navigation
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Display the selected page content
    if selection == "Home":
        st.title("Home")
        st.write(PAGES["Home"])
        st.write("Use this app to get sentiment analysis from tweets.")
    
    elif selection == "About":
        st.title("About")
        st.write(PAGES["About"])
    
    elif selection == "Prediction":
        st.title("Prediction")
        st.write(PAGES["Prediction"])
        
        # Input field for user text
        input_text = st.text_input('Enter tweet:')

        # Button to make prediction
        if st.button('Submit'):
            if input_text:
                # Send POST request to Flask API
                try:
                    response = requests.post(
                        'https://project-test-dep-7.onrender.com/predict',
                        json={'input': [input_text]},
                        headers={'Content-Type': 'application/json'}
                    )
                    response.raise_for_status()  # Check if the request was successful

                    # Parse the response
                    data = response.json()
                    prediction = data.get('prediction', [0])[0]  # Default to 0 if no prediction

                    # Display the result
                    sentiment = {
                        0: "Neutral",
                        1: "Negative",
                        2: "Positive"
                    }.get(prediction, "Unknown")
                    
                    st.write(f'Prediction: {prediction} ({sentiment})')
                except requests.exceptions.RequestException as e:
                    st.error(f'Error: {e}')
            else:
                st.warning('Please enter a tweet.')

if __name__ == "__main__":
    main()
