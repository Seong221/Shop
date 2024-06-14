FROM python:3

WORKDIR /Shop

COPY . /Shop



RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "Test2:second_test", "--host", "0.0.0.0", "--port", "8080", "--reload"]
