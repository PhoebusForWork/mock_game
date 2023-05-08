FROM python:3.9.16-slim
RUN pip3 install poetry
RUN mkdir /app
COPY  ./ /app
RUN pip3 install -r /app/requirements.txt
RUN useradd app && \
    chown app:app /app
USER app
CMD ["python3", "/app/main.py", "8888"]