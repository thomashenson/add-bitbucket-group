FROM python:3.9

RUN pip3 install requests

ADD ./update-groups.py /app/

CMD ["python3", "/app/update-groups.py"]