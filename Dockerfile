# Use a lightweight Python 3.10 slim image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /service

# Copy project files into the container
COPY . /service/

# Upgrade pip and install necessary dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        fastapi \
        uvicorn \
        pandas \
        numpy \
        catboost \
        shap \
        seaborn \
        matplotlib \
        scikit-learn \
        pyarrow \
        ipywidgets \
        gunicorn \
        streamlit

# Expose necessary ports
EXPOSE 8000 8501

# Default command to run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app_demo.py --server.port 8501 --server.address 0.0.0.0"]