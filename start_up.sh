cd src

uvicorn apis:app --port 8090 &
streamlit run webui.py --server.maxUploadSize 5000