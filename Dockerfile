FROM python
WORKDIR /app/
COPY "public" /app/
COPY "templates" /app/
COPY "app.py" /app/
COPY "requirements.txt" /app/
RUN pip install -r requirements.txt
EXPOSE 5000