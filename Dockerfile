#Sample Dockerfile for NodeJS Apps

FROM node:16

ENV NODE_ENV=production
RUN apt-get update || : && apt-get install python-pip -y
WORKDIR /work_dir

COPY . .

WORKDIR /work_dir/backend/
RUN pip3 install -r requirements.txt

WORKDIR /work_dir/frontend/

RUN npm install
RUN npm run build

EXPOSE 3000

WORKDIR /work_dir/frontend/
RUN chmod a+x run.sh
CMD ["./run.sh"]