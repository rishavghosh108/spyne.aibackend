FROM python:3.10.10-slim
WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r requirments.txt
RUN chmod +x run.sh
CMD [ "bash","run.sh" ]