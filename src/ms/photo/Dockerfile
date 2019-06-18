FROM python:3

RUN mkdir photo

WORKDIR /photo

RUN pip3 install pytest mongoengine flask connexion pillow nose

COPY . /photo

EXPOSE 8091

CMD ["python3", "photo_service_main.py"]
