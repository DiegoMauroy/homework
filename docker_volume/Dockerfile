FROM python:3.11.1

# set the working directory in the container
WORKDIR /coin

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./src/ ./src/
COPY ./data/ ./data/
COPY config.ini .

# command to run on container start
CMD ["python3", "./src/main.py"]