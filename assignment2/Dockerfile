FROM python:3.13

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 9999

ENV FLASK_ENV=production
ENV FLASK_APP=app.py

CMD ["python", "app.py"]