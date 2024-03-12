import streamlit as st
import google.generativeai as genai
import os 
import plotly.graph_objects as go
from dotenv import load_dotenv
load_dotenv()   # load env varibles 
from PIL import Image 
import json
import time

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_promt , image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_promt,image[0]])
    return response.text

def input_image_setup(upload_file):
    if upload_file is not None:
        byte_data = upload_file.getvalue()

        image_parts  = [
            {
                "mime_type" : upload_file.type,
                "data": byte_data
            }
        ]

        return image_parts  
    else :
        raise FileNotFoundError("NO File uploaded ")
    

# Set page configuration
st.set_page_config(page_title="NutriLens")
st.header("NutriLens")

def parse_gemini_response(response):
    # Parse the JSON response to extract x and y values for plotting
    data = json.loads(response)
    x_values = data["data"][0]["x"]
    y_values = data["data"][0]["y"]
    return x_values, y_values


# Define the content for each page
st.header("Let's Begin")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
col1, col2, col3 = st.columns(3)

with col1:
    submit = st.button("Get the full details of the food")

with col2:
    graph = st.button("Generate Graph of the Data")

with col3:
    piechart = st.button("Get Pie Chart")


input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and
calculate the total calories, also provide the details of every food items with calories intake in below format
1. Item 1 - no of calories
2. Item - no of calories
- - --
Generate statistical data suitable for plotting based on the image of the food items. Include information such as calories, nutrients, or any other relevant numerical data. Please provide data in a format suitable for creating a graph using Plotly.

Finally you can also mention whether the food is healthy or not and also mention the
percentage split of the ratio of carbohydrates, fats, fibers, sugar and other things required in our diet.
Suggest alternate recipes with better nutrition for the same.
"""

# Button to generate graph
# Button to generate graph
if graph:
    if uploaded_file is not None:
        # Get Gemini response
            prompt = """
            Give the details of the contents of Fat, Carbohydrates and Protein in the given format and don't add any extra text.
            {
            "data": [
                {
                "x": ["Fat", "Carbohydrates", "Protein"],
                "y": [34, 40, 18]
                }
            ]
            }
            """
            image_data = input_image_setup(uploaded_file)
            gemini_response = get_gemini_response(prompt, image_data)
            # Parse Gemini response to extract numerical data
            x_values, y_values = parse_gemini_response(gemini_response)

            # Create plotly graph
            colors = ['red', 'yellow', 'green', 'blue']
            fig = go.Figure(data=[go.Bar(x=x_values, y=y_values, marker_color=colors)])
            fig.update_layout(title='Nutritional Information', xaxis_title='Nutrient', yaxis_title='Amount')

            # Display the plot
            st.plotly_chart(fig)
    else:
            st.error("Please upload an image first.")
    
if piechart:
    if uploaded_file is not None:
                # Get Gemini response
            prompt = """
            Give the details of the contents of Fat, Carbohydrates and Protein in the given format and don't add any extra text.
            {
            "data": [
                {
                "x": ["Fat", "Carbohydrates", "Protein"],
                "y": [34, 40, 18]
                }
            ]
            }
            """
            image_data = input_image_setup(uploaded_file)
            gemini_response = get_gemini_response(prompt, image_data)
            # Parse Gemini response to extract numerical data
            x_values, y_values = parse_gemini_response(gemini_response)

            # Create plotly pie chart
            colors = ['gold', 'red', 'yellowgreen', 'lightcoral']
            fig = go.Figure(data=[go.Pie(labels=x_values, values=y_values, marker=dict(colors=colors))])
            fig.update_layout(title='Nutritional Information (Pie Chart)')

            # Display the pie chart
            st.plotly_chart(fig)
    else:
        st.error("Please upload an image first.")


if submit:
    if uploaded_file is not None: 
            image_data= input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt,image_data)
            st.header("Full Description about the food are...")
            st.write(response)
    else:
        st.error("Please upload an image first.")