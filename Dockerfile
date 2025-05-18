FROM apache/flink:2.0.0-scala_2.12-java17

# Python 3.11 설치
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev python3.11-distutils curl && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# 환경 변수 설정
ENV PYTHON_VERSION=3.11
ENV PYFLINK_PYTHON=/usr/bin/python3

# 필요한 Python 패키지 설치 (requirements.txt 사용)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# PyFlink 앱 복사
WORKDIR /opt/flink/app
COPY flink_app.py .

# 실행 명령
CMD ["flink", "run", "-py", "flink_app.py"]
