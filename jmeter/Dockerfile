FROM openjdk:11-jre-slim

ENV JMETER_VERSION=5.4.1
ENV JMETER_HOME=/opt/apache-jmeter-${JMETER_VERSION}
ENV PATH=${JMETER_HOME}/bin:$PATH

RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz && \
    tar -xzf apache-jmeter-${JMETER_VERSION}.tgz -C /opt/ && \
    rm apache-jmeter-${JMETER_VERSION}.tgz

WORKDIR ${JMETER_HOME}

# Provide the project-specific test plan inside the image
COPY fastapi_test_plan.jmx ${JMETER_HOME}/fastapi_test_plan.jmx

# Default entrypoint runs JMeter; Jenkins overrides arguments as needed
ENTRYPOINT ["jmeter"]
