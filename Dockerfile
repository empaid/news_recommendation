#Sample Dockerfile for NodeJS Apps

FROM node:16

ENV NODE_ENV=production

WORKDIR /work_dir

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install

COPY . .
RUN npm run build

EXPOSE 8080

CMD [ "npm", "start"]