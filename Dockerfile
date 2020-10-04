FROM frolvlad/alpine-miniconda3

# Hack this should be dynamically set.. 
ENV PATH $PATH:/home/checkpy/.local/bin

RUN /opt/conda/bin/conda install --yes --freeze-installed \
       numpy nomkl matplotlib \
       && /opt/conda/bin/conda clean -afy
COPY requirements.txt .
RUN pip install -r requirements.txt

#
# Everything below will run as unprived checkpy user
#
RUN addgroup -S checkpy && adduser -S checkpy -G checkpy
USER checkpy

# Add local folder (pip install --user) to PATH
RUN export PY_USER_BIN=$(python -c 'import site; print(site.USER_BASE + "/bin")')
RUN export PATH=$PY_USER_BIN:$PATH

# install checkpy in local folder (will write test DB to that folder)
RUN pip install --user checkpy
#RUN checkpy -register /base/tests
RUN checkpy -d uva/progns

