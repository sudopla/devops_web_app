
FROM centos
EXPOSE 80
RUN \
  yum update -y && \
  yum install git -y && \
  yum install nginx -y && \
  yum install python3 -y && \ 
  pip3 install PyGithub &&\
  pip3 install gitpython &&\
  pip3 install datadog &&\
  pip3 install gunicorn && \
  pip3 install django

COPY app_code/ /usr/src/app/
COPY nginx.conf /etc/nginx/
COPY init_script.sh init_script.sh
CMD ["/init_script.sh"]
