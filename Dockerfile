FROM jupyter/minimal-notebook

USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk \
    && pip install ipywidgets SPARQLWrapper

USER jovyan
WORKDIR /home/jovyan/work

COPY DmfAXML2RDF.ipynb validate.ipynb fullQuadStore.nq.gz /home/jovyan/work
COPY common /home/jovyan/work/common
COPY DMFA /home/jovyan/work/DMFA
COPY DMFAREQ /home/jovyan/work/DMFAREQ
RUN mkdir package

RUN mkdir package/rmlmapper \
    && wget -O package/rmlmapper/rmlmapper.jar https://github.com/RMLio/rmlmapper-java/releases/download/v6.1.3/rmlmapper-6.1.3-r367-all.jar

RUN wget -O package/apache-jena-fuseki.tar.gz https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.8.0.tar.gz && \
    tar -xzf package/apache-jena-fuseki.tar.gz && \
    mv apache-jena-fuseki-* package/apache-jena-fuseki && \
    rm package/apache-jena-fuseki.tar.gz
    
RUN wget -O package/shaclvalidator.zip https://repo1.maven.org/maven2/org/topbraid/shacl/1.4.2/shacl-1.4.2-bin.zip && \
    unzip package/shaclvalidator.zip -d package && \
    mv package/shacl-* package/shaclvalidator && \
    rm package/shaclvalidator.zip

RUN chmod +x package/shaclvalidator/bin/shaclvalidate.sh
ENV PATH="/home/jovyan/work/package/shaclvalidator/bin:${PATH}"

EXPOSE 8888 3030

CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password='' --allow-root & package/apache-jena-fuseki/fuseki-server --file=fullQuadStore.nq.gz /socialsecurity"]
