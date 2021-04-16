FROM python:3
EXPOSE 8000
ADD convokit /convokit
COPY requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/convokit"
ENTRYPOINT python3 -m http.server --directory /convokit/supreme/results