# 使用 Ubuntu 20.04 作為基礎映像檔
FROM ubuntu:22.04

# 設定非互動模式，避免安裝過程中的提示
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# 更新套件列表，並安裝 Python 3.9 以及 pip（Python 套件管理工具）
RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get install software-properties-common curl build-essential pkg-config -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install python3.9 python3.9-distutils python3.9-venv python3.9-dev -y && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    curl -sS https://bootstrap.pypa.io/pip/3.9/get-pip.py | python3.9

# 設定優先使用預編譯二進制包
ENV PIP_PREFER_BINARY=1

# 安裝 pipenv
RUN python3.9 -m pip install --upgrade pip pipenv

# 建立工作目錄 /dataflow
RUN mkdir /dataflow

# 先複製 Pipfile (如果之後有 Pipfile.lock 也會複製)
COPY ./Pipfile /dataflow/
COPY ./Pipfile.lock* /dataflow/

# 將其他檔案複製到容器
COPY ./src /dataflow/src
COPY ./setup.py /dataflow
COPY ./genenv.py /dataflow
COPY ./README.md /dataflow
COPY ./local.ini /dataflow
COPY ./airflow-gce.cfg /dataflow

# # 設定容器的工作目錄為 /dataflow，後續的指令都在這個目錄下執行
WORKDIR /dataflow/

# # 安裝依賴（使用 pip 直接安裝以避免 pipenv 編譯問題）
RUN pip3 install pandas sqlalchemy pymysql==1.0.2 loguru==0.6.0 \
    apache-airflow==2.7.3 apache-airflow-providers-docker==3.0.0 \
    "celery[redis]" flower==1.0.0 apache-airflow-providers-celery==3.6.0 \
    apache-airflow-providers-google==10.17.0 google-cloud-storage==2.16.0 \
    flask-session==0.5.0 mysql-connector-python

# 安裝本地套件
RUN pip3 install -e .

# # 設定語系環境變數，避免 Python 編碼問題
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN echo "UTC" > /etc/timezone

# # 建立 .env
# RUN ENV=PRODUCTION python3 genenv.py

# airflow
ARG AIRFLOW_USER_HOME=/dataflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV AIRFLOW_CONFIG=/dataflow/airflow-gce.cfg

# # 啟動容器後，預設執行 bash（開啟終端）
# 需要由外部（compose / DockerOperator）寫指定 command 告訴 service/container 要執行什麼
CMD ["/bin/bash"]
