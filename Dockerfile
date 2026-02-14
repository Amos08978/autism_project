# 使用官方 Python 映像檔作為基礎
FROM python:3.11-slim

# 設定容器內的工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案到容器中
COPY . .

# 設定啟動指令，使用 gunicorn 啟動 Flask 應用
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]