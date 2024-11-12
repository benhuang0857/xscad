# 使用官方的 Python 基礎映像
FROM python:3.9-slim

# 安裝必要的工具和庫，包括 binutils
RUN apt-get update && apt-get install -y \
    protobuf-compiler \
    binutils \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 的打包工具 PyInstaller
RUN pip install pyinstaller

# 設定工作目錄
WORKDIR /app

# 複製需求文件並安裝依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製伺服器代碼和 .proto 文件
COPY . .

# 編譯 .proto 文件
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. xscad.proto

# 使用 PyInstaller 將 server.py 編譯成二進制可執行文件
RUN pyinstaller --onefile server.py

# 曝露伺服器運行的端口
EXPOSE 50051

# 使用編譯好的二進制文件啟動伺服器
CMD ["./dist/server"]
