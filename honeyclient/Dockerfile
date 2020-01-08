FROM python:3.6

WORKDIR /usr/src/tr069
COPY . .
RUN pip3 install --no-cache-dir -e .[pretty]
ENTRYPOINT ["tr069-client"]
CMD ["http://acs:7547/"]
