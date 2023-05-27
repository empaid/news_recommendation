#Sample Dockerfile for NodeJS Apps

FROM node:16

ENV NODE_ENV=production

WORKDIR /work_dir

COPY . .
WORKDIR /work_dir/frontend/

RUN npm install
RUN npm run build

EXPOSE 8080

CMD [ "npm", "start"]