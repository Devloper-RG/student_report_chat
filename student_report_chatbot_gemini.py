import google.generativeai as genai
import json
import streamlit as st


genai_model = r'gemini-1.0-pro-latest' 

class RAG():


  def __init__(self):
    
        print("inside RAG")
        self.genai(genai_model)
    


  def load_json(self,student):
        
        print("inside load_json")
        with open(f'./document/{student}.json') as f:
            self.data = json.load(f)
        self.chat_genai()


  def genai(self,model_name):

        genai.configure(api_key= st.secrets["gen_ai_api_key"])
        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        generation_config = genai.GenerationConfig(
        stop_sequences = None,
        temperature=0.0,
        top_p=0.9,
        top_k=32,
        candidate_count=1,
        # max_output_tokens=500,
        )
        self.model = genai.GenerativeModel(model_name, safety_settings = safety_settings,generation_config=generation_config)

  def chat_genai(self):
    
    self.chat = self.model.start_chat(history=[])
    self.chat.send_message(f"""
    PAT report information is below.
    ---------------------
    {str(self.data)}
    ---------------------
    INSTRUCTION: 
    1. Use the PAT report information and DO NOT USE YOUR PRIOR KNOWLEDGE.
    2. Answer the questions in 5 to 10 lines based on PAT report provided. 
    3. DO NOT GIVE RESPONSES THAT STATES YOU HAVE GIVEN RESPONSE USING THE CONTEXT PROVIDED.
    """)
      #f"Completely understand the student from report provided below.report = {self.data}.Instruction: Do not your knowledge,Generate only on the bases of the report provided")

    
  def response_genai(self,query):

        print("inside response_genai")
        response = self.chat.send_message(query) 
        return response.text

  
rag_instance = RAG()

def get_json(student):
  rag_instance.load_json(student)


def chat_response(prompt):
  response = rag_instance.response_genai(prompt)
  print(response)
  return response
