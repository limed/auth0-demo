FROM python
MAINTAINER limed@mozilla.com

COPY app /app
COPY config.py /app
WORKDIR /app
RUN pip install -r requirements.txt

VOLUME /app
EXPOSE 8080

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
