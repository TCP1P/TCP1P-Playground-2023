FROM node:latest

WORKDIR /app
COPY ./server/package.json .
RUN npm i
COPY ./server .
ENV FLAG="fakeflag{}"
RUN npm run build
CMD ["npm", "run", "start"]
