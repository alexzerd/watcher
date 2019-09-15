FROM python
RUN pip install kubernetes
WORKDIR /watcher
COPY * /watcher/
CMD ["python", "watcher.py"]
