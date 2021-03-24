# set base image (host OS)
FROM python:3.8-slim-buster



# set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc unixodbc-dev \
    unixodbc \
    libpq-dev \
	g++ \	
	make \
    cmake \
    mariadb-client \
	default-mysql-client \
    gnupg2


# Setup dependencies for pyodbc
RUN \
  export ACCEPT_EULA='Y' && \
  export MYSQL_CONNECTOR='mysql-connector-odbc-8.0.18-linux-glibc2.12-x86-64bit' && \
  export MYSQL_CONNECTOR_CHECKSUM='f2684bb246db22f2c9c440c4d905dde9' && \
  apt-get update && \
  apt-get install -y curl build-essential unixodbc-dev g++ apt-transport-https && \
  gpg --keyserver hkp://keys.gnupg.net --recv-keys 5072E1F5 && \
  #
  # Install pyodbc db drivers for MSSQL, PG and MySQL
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
  curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
  curl -L -o ${MYSQL_CONNECTOR}.tar.gz https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/${MYSQL_CONNECTOR}.tar.gz && \
  curl -L -o ${MYSQL_CONNECTOR}.tar.gz.asc https://downloads.mysql.com/archives/gpg/\?file\=${MYSQL_CONNECTOR}.tar.gz\&p\=10 && \
  gpg --verify ${MYSQL_CONNECTOR}.tar.gz.asc && \
  echo "${MYSQL_CONNECTOR_CHECKSUM} ${MYSQL_CONNECTOR}.tar.gz" | md5sum -c - && \
  
  
  
  
  apt-get update && \
  gunzip ${MYSQL_CONNECTOR}.tar.gz && tar xvf ${MYSQL_CONNECTOR}.tar && \
  cp ${MYSQL_CONNECTOR}/bin/* /usr/local/bin && cp ${MYSQL_CONNECTOR}/lib/* /usr/local/lib && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0 Driver" -t "Driver=/usr/local/lib/libmyodbc8w.so" && \
  myodbc-installer -a -d -n "MySQL ODBC 8.0" -t "Driver=/usr/local/lib/libmyodbc8a.so" && \
  apt-get install -y msodbcsql17 odbc-postgresql && \
  #
  # Update odbcinst.ini to make sure full path to driver is listed
  sed 's/Driver=psql/Driver=\/usr\/lib\/x86_64-linux-gnu\/odbc\/psql/' /etc/odbcinst.ini > /tmp/temp.ini && \
  mv -f /tmp/temp.ini /etc/odbcinst.ini && \
  # Install dependencies
  pip install --upgrade pip



# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get -y install gcc g++

# install dependencies
RUN pip3 install -r requirements.txt


# copy the content of the local src directory to the working directory
COPY ./src .


EXPOSE 5000


# command to run on container start
CMD [ "python", "./index.py", "--host=0.0.0.0", "-p", "5000" ]
