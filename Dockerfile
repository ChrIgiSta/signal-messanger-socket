# Build Signal socket docker in a debian env

# autor: Christian Stauffer
# date:  03.03.2020, Frauenfeld


FROM debian:stretch

RUN apt-get update
RUN apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install gradle default-jdk python
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git

RUN git clone https://github.com/AsamK/signal-cli.git /var/signal
WORKDIR "/var/signal"
RUN ./gradlew build
RUN ./gradlew installDist
RUN ./gradlew distTar

RUN apt-get install -y python-simplejson

# Expose port
EXPOSE 16323

ADD signal_socket.py /var/signal_socket.py
WORKDIR "/var/"

CMD python signal_socket.py
