FROM eclipse-temurin:11-jre

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Install JMeter
ENV JMETER_VERSION 5.4.1
RUN wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz && \
    tar -xzf apache-jmeter-$JMETER_VERSION.tgz -C /opt/ && \
    rm apache-jmeter-$JMETER_VERSION.tgz

ENV JMETER_HOME /opt/apache-jmeter-$JMETER_VERSION
ENV PATH $JMETER_HOME/bin:$PATH

WORKDIR $JMETER_HOME

