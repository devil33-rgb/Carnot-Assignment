FROM python:latest

COPY ./requirements.txt /tmp/requirements.txt
COPY ./carnot /carnot
WORKDIR /carnot
EXPOSE 8000


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp   


ENV PATH="/py/bin:$PATH"

CMD ["python", "manage.py","runserver","0.0.0.0","8000"]



