import google.generativeai as genai
# Paste your key here just for the test
genai.configure(api_key="api")

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)