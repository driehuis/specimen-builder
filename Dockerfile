# docker build . -t specimen-builder
# docker run --rm -v `pwd`/src:/app/src -v `pwd`/out:/out specimen-builder
FROM node:12

COPY package.json yarn.lock /app/
RUN cd /app \
    && yarn install --pure-lockfile

COPY . /app/
EXPOSE 3001
#CMD cd /app && yarn fontdata && yarn build && cp -pr _site /out/
CMD cd /app && yarn build && cp -pr _site /out/
