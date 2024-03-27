from serpapi import GoogleSearch
from openai import OpenAI
import os

OpenAI.api_key = os.getenv('OPENAI_API_KEY')
CLIENT = OpenAI()

GoogleSearch.SERP_API_KEY = os.getenv('SERP_API_KEY')
