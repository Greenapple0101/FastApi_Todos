FROM justb4/jmeter:5.4.1

WORKDIR /tests

# Copy the FastAPI load-test plan into the image so it is available at runtime
COPY fastapi_test_plan.jmx /tests/fastapi_test_plan.jmx

# Override upstream entrypoint so Jenkins can set the exact command
ENTRYPOINT [""]

# Provide a sensible default; Jenkins overrides this via the stage command
CMD ["-n", "-t", "/tests/fastapi_test_plan.jmx", "-l", "/tests/results.jtl"]
