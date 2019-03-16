FROM python:3.7.2-stretch

WORKDIR /app

RUN mkdir -p src

COPY src/requirements.in src/
COPY src/requirements.txt src/

RUN pip install --no-cache-dir pip-tools
RUN pip-compile --output-file src/requirements.txt src/requirements.in
RUN pip install --no-cache-dir -r src/requirements.txt

COPY . .

CMD ["python", "src/main.py"]
