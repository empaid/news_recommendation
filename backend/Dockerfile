#Sample Dockerfile for NodeJS Apps

FROM python



COPY . .

WORKDIR /
RUN pip install -r requirements.txt


EXPOSE 5000

CMD python index.py