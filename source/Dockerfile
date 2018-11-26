FROM python:3.6


ENV source_path /opt/program/source
RUN mkdir -p ${source_path}

#Sagemaker
RUN mkdir -p /opt/ml/


#Set up source
COPY ./  ${source_path}
RUN pip install -r ${source_path}/requirements.txt -t ${source_path}
RUN pip install  awscli --upgrade

#Set up working directory
WORKDIR ${source_path}
ENTRYPOINT  ["python", "sagemaker_entry.py"]

#Default arguments to run test
CMD ["train"]
