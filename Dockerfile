FROM my_miniconda:latest

# Set the working directory
WORKDIR /opt

# Set up environment variables
ENV PATH=/srv/miniconda3/bin:$PATH

# Install dependencies and tools
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends --no-install-suggests \
    wget \
    bzip2 \
    git \
    vim \
    locales \
    build-essential \
    libgfortran5 \
    zip \
    && apt-get autoremove -y \
    && apt-get clean -y

# Create the Conda environment from environment.yml
COPY environment1.yml /opt/environment.yml
RUN conda env create -f /opt/environment.yml

# Ensure the environment is activated by default
RUN echo "source activate oilspill001" >> ~/.bashrc

# Set working directory for the application
WORKDIR /

# Copy the application files
COPY src/.env .env
COPY src/main1_image_download.py /oilspill001/src/oilspill001/main.py
COPY src/module_asf.py /oilspill001/src/oilspill001/
COPY src/module_log.py /oilspill001/src/oilspill001/
COPY src/__init__.py /oilspill001/src/oilspill001/
COPY pyproject.toml /oilspill001/
COPY setup.py /oilspill001/setup.py
COPY README.md /oilspill001/README.md

# Install the application using Conda's pip
RUN /bin/bash -c "source activate oilspill001 && pip install -U /oilspill001"

# Reduce the image size
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /src /var/lib/apt/lists/*

# Default command
CMD [ "bash", "-c", "source activate oilspill001 && exec /bin/bash" ]