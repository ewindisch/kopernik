FROM python:3.4.3-onbuild
MAINTAINER Eric Windisch

ENV PYTHONPATH .
EXPOSE 80

CMD ["python", "kopernik/endpoint.py"]
