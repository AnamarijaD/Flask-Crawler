FROM python:3.9.0a6-buster

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app
# RUN apk add --update curl gcc g++
# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev
# install the dependencies and packages in the requirements file
# RUN apt-get update && \
#     apt-get -y install python3-pandas
RUN pip install --upgrade pip
# RUN pip install --upgrade cython
RUN pip install --no-cache-dir -r ./requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]