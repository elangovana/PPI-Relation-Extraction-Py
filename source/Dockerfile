FROM python:3.6-alpine
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h


ENV source_path /opt/program/source
RUN mkdir -p ${source_path}



#Set up source
COPY ./  ${source_path}
RUN pip install -r ${source_path}/requirements.txt -t ${source_path}
RUN pip install  awscli --upgrade

#Set up working directory
WORKDIR ${source_path}
ENTRYPOINT  ["python"]

#Default arguments to run test
CMD ["main.py", "."]
