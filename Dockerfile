#Sample Dockerfile for NodeJS Apps

FROM node:16

ENV NODE_ENV=production

WORKDIR /work_dir

RUN npm install

COPY . .
WORKDIR /work_dir/frontend/
RUN npm run build

EXPOSE 8080

CMD [ "npm", "start"]