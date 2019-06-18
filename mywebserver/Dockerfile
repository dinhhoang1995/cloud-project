FROM python:3
RUN mkdir data
ADD file1.html /data/file1.html
ADD file2.html /data/file2.html
ADD file3.html /data/file3.html
WORKDIR /data
CMD python3 -m http.server 8080
