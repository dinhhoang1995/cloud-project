FROM python:3

RUN mkdir photographer

WORKDIR /photographer

RUN pip3 install pytest mongoengine flask connexion

COPY . /photographer

EXPOSE 8090

CMD ["python3", "photographer_service_main.py"]
