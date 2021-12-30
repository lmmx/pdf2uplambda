# Note: use `docker run --rm -it mlupin/docker-lambda:python3.9-build /bin/bash` to get a shell
FROM public.ecr.aws/lambda/python:3.9

COPY ./*.py "${LAMBDA_TASK_ROOT}"/
RUN ls -la "${LAMBDA_TASK_ROOT}"/*.py

COPY requirements.txt  .
RUN yum install -y poppler-utils
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "lambda_function.lambda_handler" ]
