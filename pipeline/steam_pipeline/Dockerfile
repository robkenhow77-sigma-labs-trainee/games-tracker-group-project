FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

# Installing chrome
RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm jq unzip
# Copy and run the chrome installer script
COPY ./chrome-installer.sh ./chrome-installer.sh
RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN rm ./chrome-installer.sh

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY steam_extract.py .

COPY steam_transform.py .

COPY steam_load.py .

COPY steam_load_functions.py .

COPY steam_pipeline.py .

CMD ["steam_pipeline.lambda_handler"]