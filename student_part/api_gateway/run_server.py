import uvicorn
# Комментарий от шкебеде
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.4", port=8005, log_level="info", reload=True)