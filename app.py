import streamlit as st
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv
import os

from companies import companies

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

st.title("AI GTM Automation Dashboard")

results = []

for company in companies:

    name = company["name"]
    description = company["description"]
    employees = company["employees"]

    # Segmentation Logic
    if employees < 200:
        segment = "SMB"
    else:
        segment = "Enterprise"

    # AI Prompt
    prompt = f"""
    Company: {name}
    Description:{description}
    Segment: {segment}
    Generate:
    1. One short use case
    2. One cold email
    3. One LinkedIn DM
    """

    response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    max_tokens=300,
    temperature=0.7,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

    output = response.choices[0].message.content

    # Pipeline value logic
    if segment == "Enterprise":
        pipeline_value = "$50,000"
    else:
        pipeline_value = "$5,000"

    results.append({
        "Company": name,
        "Segment": segment,
        "Employees": employees,
        "Pipeline Value": pipeline_value,
        "AI Output": output
    })

df = pd.DataFrame(results)

st.dataframe(df)