


FROM ubuntu:24.04
# latest
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-get install -y openjdk-11-jre  \
    # && apt-get install openjfx -y\
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*


# FROM openjdk:21
# RUN microdnf update \
#     && apt-get install -y software-properties-common \
#     && microdnf install --nodocs wget unzip \
#     && microdnf clean all \
#     && rm -rf /var/cache/yum

# RUN username="quickhmi" \
#     password="indi" \
#     pass=$(perl -e 'print crypt($ARGV[0], "password")' $password) \
#     useradd -m -p $pass $username

RUN useradd -m quickhmi && echo "quickhmi:indi" | chpasswd

WORKDIR /home/quickhmi

# COPY QuickHMI-test.qexp /home/quickhmi
# COPY QuickHMIServer.tar /home/quickhmi
# COPY . /home/quickhmi/
# RUN wget https://www.quickhmi.de/linux/gazelle/QuickHMIServer.tar 
RUN wget https://www.quickhmi.de/linux/hawk/QuickHMIServer.tar

RUN tar -xvf QuickHMIServer.tar 
#\
    # && rm QuickHMIServer.tar 


RUN chown -R quickhmi:quickhmi QuickHMIServer
# RUN ls -a QuickHMIServer \
#     && sleep 20

# COPY QuickHMI-test.qexp QuickHMIServer/
COPY QuickHMI-test.qexp /home/quickhmi/QuickHMIServer
COPY QuickHMI.qexp /home/quickhmi/QuickHMIServer
COPY start.sh /home/quickhmi/QuickHMIServer
COPY QuickHMIServer/. /home/quickhmi/QuickHMIServer

RUN cp -a QuickHMIServer/usr/. /usr/

# RUN ls /etc/init.d \
#     && sleep 10
# RUN mkdir /etc
# RUN cp -a QuickHMIServer/etc/. /etc/
RUN cp -a QuickHMIServer/etc/init.d/. /etc/init.d/
# RUN rm -rf QuickHMIServer/etc

WORKDIR /home/quickhmi/QuickHMIServer

RUN    sh qhmiRM.sh -v
#     # && sh qhmiRM.sh -u \
#     # && sh qhmiRM.sh -v \
#     # && sleep 5
#     && sh qhmiRM.sh -i QuickHMI-test.qexp
    # && sh qhmiRM.sh -v \
    # && sh qhmiRM.sh -u \
    # && sh qhmiRM.sh -v

# RUN sh qhmiRM.sh -i QuickHMI-test.qexp

# CMD sleep 10\
    # && sh qhmiRM.sh -i QuickHMI-test.qexp \
    # && /home/quickhmi/QuickHMIServer/qhmiRM.sh -i /home/quickhmi/QuickHMI-test.qexp \
    # && /home/quickhmi/QuickHMIServer/qhmiRM.sh -rd
# CMD sh qhmiRM.sh -rd 
    # && sleep 120000

CMD sh start.sh 
# CMD sh qhmiRM.sh -i QuickHMI-test.qexp &&\
#     sh qhmiRM.sh -rd &&\
#     sleep 120000
    # tail -F /var/log/mysql/error.log

# RUN /home/quickhmi/QuickHMIServer/qhmiRM.sh -v \
#     /home/quickhmi/QuickHMIServer/qhmiRM.sh -u \
#     /home/quickhmi/QuickHMIServer/qhmiRM.sh -v \
#     && sleep 25
#     # && /home/quickhmi/QuickHMIServer/qhmiRM.sh -i /home/quickhmi/QuickHMI-test.qexp 


# CMD sleep 10\
#     && ls\
#     # && /home/quickhmi/QuickHMIServer/qhmiRM.sh -i /home/quickhmi/QuickHMI-test.qexp \
#     # && /home/quickhmi/QuickHMIServer/qhmiRM.sh -rd
# # CMD /home/quickhmi/QuickHMIServer/qhmiRM.sh -rd 
#     && sleep 1200
