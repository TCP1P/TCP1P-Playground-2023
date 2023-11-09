FROM node:latest

WORKDIR /app
COPY ./server/package.json .
RUN npm i
COPY ./server .
ENV FLAG="TCP1P{prototype_polution_is_pretty_common_right?}"
RUN npm run build
CMD ["npm", "run", "start"]
