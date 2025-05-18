cd src

uvicorn apis:app --port 8090 &
python webui.py
# streamlit run webui.py --server.maxUploadSize 5000