#Sample Dockerfile for NodeJS Apps

FROM node:16

ENV NODE_ENV=production
WORKDIR /

COPY . .

RUN npm install
RUN npm run build

EXPOSE 3000

CMD npm start