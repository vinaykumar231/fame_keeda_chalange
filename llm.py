import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from pydantic import BaseModel




load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# ---------------------- LLM Integration ----------------------

def generate_campaign_brief(prompt: str):
    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",  
            system_instruction="You are a marketing assistant.",
        )
        response = model.generate_content(prompt, request_options={"timeout": 600})
        return response.text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")
