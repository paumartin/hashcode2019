FROM python:3.6.8-jessie
WORKDIR /code
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD . ./
CMD ["python", "solution.py"]