FROM floodio/jmeter:5.6.2
WORKDIR /tests



WORKDIR /tests

# Copy the FastAPI load-test plan into the image
COPY fastapi_test_plan.jmx /tests/fastapi_test_plan.jmx

# Default command executes the bundled JMX in non-GUI mode and stores results
CMD ["-n", "-t", "/tests/fastapi_test_plan.jmx", "-l", "/tests/results.jtl"]

