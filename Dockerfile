FROM registry.access.redhat.com/ubi8/python-36:latest
USER root
WORKDIR /htdocs
RUN yum install -y python3-pyyaml
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-Bottleneck-1.2.1-13.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-numexpr-2.7.0-3.el8.x86_64.rpm
RUN yum install -y https://vault.centos.org/centos/8/BaseOS/x86_64/os/Packages/snappy-1.1.8-3.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/b/blosc-1.17.0-2.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/h/hdf5-1.10.5-4.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-tables-3.5.2-6.el8.x86_64.rpm
RUN yum install -y https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/python3-cairo-1.16.3-6.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-kiwisolver-1.1.0-3.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-cycler-0.10.0-11.el8.noarch.rpm
RUN yum install -y https://vault.centos.org/centos/8/PowerTools/x86_64/os/Packages/libqhull-2015.2-5.el8.x86_64.rpm
RUN yum install -y http://repo.okay.com.mx/centos/8/x86_64/release/texlive-lib-20180414-13.el8.x86_64.rpm
RUN yum install -y http://repo.okay.com.mx/centos/8/x86_64/release/texlive-kpathsea-20180414-13.el8.x86_64.rpm
RUN yum install -y http://repo.okay.com.mx/centos/8/x86_64/release/texlive-base-20180414-13.el8.noarch.rpm
RUN yum install -y http://repo.okay.com.mx/centos/8/x86_64/release/texlive-dvipng-20180414-13.el8.x86_64.rpm
RUN yum install -y https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/texlive-dvipng-20180414-23.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-matplotlib-data-3.0.3-4.el8.noarch.rpm https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-matplotlib-data-fonts-3.0.3-4.el8.noarch.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-matplotlib-tk-3.0.3-4.el8.x86_64.rpm https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-matplotlib-3.0.3-4.el8.x86_64.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-pandas-0.25.3-1.el8.x86_64.rpm
RUN yum install -y https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/python3-click-6.7-8.el8.noarch.rpm
RUN yum install -y https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/python3-itsdangerous-0.24-14.el8.noarch.rpm
RUN yum install -y https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/python3-werkzeug-0.12.2-4.el8.noarch.rpm
RUN yum install -y https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/python3-flask-0.12.2-4.el8.noarch.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-zipp-0.5.1-3.el8.noarch.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-certifi-2018.10.15-7.el8.noarch.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-dataclasses-0.8-3.el8.noarch.rpm
RUN yum install -y https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/p/python3-typing-extensions-3.7.4.3-2.el8.noarch.rpm
RUN yum install -y python3-mod_wsgi
#httpd

COPY requirements.txt .
RUN mkdir ./lib
#RUN /usr/bin/pip3 install -t lib -r requirements.txt

COPY *json* ./
COPY *.js ./
RUN npm install .

COPY . .

#ENV PYTHONPATH "${PYTHONPATH}:/usr/bin/python3"

#CMD python prep.py
