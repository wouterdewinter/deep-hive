FROM ubuntu:16.04

RUN apt-get -qq update && apt-get -qq -y install curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && apt-get -qq -y remove curl bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes

ENV PATH /opt/conda/bin:$PATH

ENTRYPOINT [ "/bin/bash", "-c" ]

# Create environment with dependancies
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Install CPU optimized tensorflow package
RUN /bin/bash -c "source activate deeplearning && pip install --ignore-installed --upgrade https://github.com/sigilioso/tensorflow-build/raw/master/tensorflow-1.4.0-cp36-cp36m-linux_x86_64.whl"

# Create working dir
COPY . /opt/src
WORKDIR /opt/src