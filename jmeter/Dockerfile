FROM justb4/jmeter:5.5

ENTRYPOINT [""]

WORKDIR /tests

# Copy the FastAPI load-test plan into the image so it is available at runtime
COPY fastapi_test_plan.jmx /tests/fastapi_test_plan.jmx

# Provide a sensible default; Jenkins overrides this via the stage command
CMD ["-n", "-t", "/tests/fastapi_test_plan.jmx", "-l", "/tests/results.jtl"]
