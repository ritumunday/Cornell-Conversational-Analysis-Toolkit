FROM python:3
ADD convokit /
COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3" ]
