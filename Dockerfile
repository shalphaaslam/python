FROM ubuntu

RUN apt update

RUN apt install python3-pip -y

RUN pip3 install flask

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
