import uvicorn


if __name__=="__main__":
    uvicorn.run("src.app:app",host='0.0.0.0', port=5001, reload=True, debug=True, workers=3)