from flask import Flask, render_template, request
import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

# Function to filter DataFrame based on user input and language
def filter_data(user_input, language):
    if language == 'English':
        file_path = 'IPC DATASET.xlsx'
        df = pd.read_excel(file_path)
        filtered_df = df[df.apply(lambda row: str(user_input) in str(row['SECTION_ID']) or
                                        user_input.lower() in row['SECTION_NAME'].lower() or
                                        user_input.lower() in row['DESCRIPTION'].lower() or
                                        user_input.lower() in row['PUNISHMENT'].lower(), axis=1)]
    elif language == 'Hindi':
        file_path = 'Hindi_Dataset.xlsx'
        df = pd.read_excel(file_path)
        filtered_df = df[df.apply(lambda row: str(user_input) in str(row['अनुभाग_आईडी']) or
                                        user_input.lower() in row['अनुभाग_शीर्षक'].lower() or
                                        user_input.lower() in row['विवरण'].lower() or
                                        user_input.lower() in row['सज़ा'].lower(), axis=1)]
    elif language == 'Marathi':
        file_path = 'Marathi_Dataset.xlsx'
        df = pd.read_excel(file_path)
        filtered_df = df[df.apply(lambda row: str(user_input) in str(row['विभाग_आयडी']) or
                                        user_input.lower() in row['विभाग_शीर्षक'].lower() or
                                        user_input.lower() in row['वर्णन'].lower() or
                                        user_input.lower() in row['शिक्षा'].lower(), axis=1)]
    else:
        return None

    return filtered_df

# Function to transliterate English to Devanagari (common for Hindi and Marathi)
def transliterate_to_devanagari(word):
    return transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
    user_input = request.form['user_input']
    language = request.form['language']

    # Check if the input needs transliteration
    if language in ['Hindi', 'Marathi']:
        user_input = transliterate_to_devanagari(user_input)

    # Filter the DataFrame based on user input and language
    filtered_df = filter_data(user_input, language)

    if filtered_df is None:
        return "Invalid language selected."

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        no_results_message = '<p style="color: red;">No results found.</p>'
        return render_template('result.html', result_html=no_results_message)

    # Convert the DataFrame to HTML and pass it to result.html
    result_html = filtered_df.to_html(classes='table table-striped', index=False)
    return render_template('result.html', result_html=result_html)

if __name__ == '__main__':
    app.run(debug=True)
