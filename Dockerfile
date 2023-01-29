FROM python
WORKDIR /app
COPY "public" /app/public
COPY "templates" /app/templates
COPY "app.py" /app
COPY "requirements.txt" /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EXPOSE 5000