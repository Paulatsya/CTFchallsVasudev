FROM ubuntu:latest

# Install some libs
RUN apt-get update
RUN apt-get -y install python3 python3-pip

# create ctf-user
RUN groupadd -r ctf && useradd -r -g ctf ctf

#add chall items
COPY requirements.txt /home/ctf/requirements.txt
COPY server.py /home/ctf/server.py

#set some proper permissions
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/server.py
RUN chmod 440 /home/ctf/requirements.txt

RUN python3 -m pip install --break-system-packages -r /home/ctf/requirements.txt

USER ctf
CMD ["python3", "server.py"]
