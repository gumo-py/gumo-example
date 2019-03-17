FROM node:8.15.1-stretch

RUN yarn global add google-cloud-gui
COPY google-cloud-gui-db.json /root/.google-cloud-gui-db.json

ENV PORT 8000

CMD ["google-cloud-gui", "--skip-browser", "--port=$PORT"]
