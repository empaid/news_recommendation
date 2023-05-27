#Sample Dockerfile for NodeJS Apps

FROM python:3.8

ENV NODE_ENV=production
WORKDIR /work_dir

COPY . .

WORKDIR /work_dir/backend/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:index"]