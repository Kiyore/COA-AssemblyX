FROM debian:bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    nasm \
    spim \
    qemu-user \
    gcc \
    binutils-arm-linux-gnueabi \
    gcc-arm-linux-gnueabi \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose your backend port
EXPOSE 5001

# Start the Flask app
CMD ["python3", "cloud_backend.py"]
