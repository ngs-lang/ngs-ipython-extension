FROM jupyter/scipy-notebook

USER root
RUN apt-get update --yes && apt-get install -y curl

RUN curl https://ngs-lang.org/install.sh | bash

RUN echo '{"cells":[{"cell_type":"code","execution_count":null,"id":"18460b1e","metadata":{},"outputs":[],"source":["!curl https:\/\/raw.githubusercontent.com\/ngs-lang\/ngs-ipython-extension\/master\/ngs-install.sh | bash\n","%reload_ext ngs"]},{"cell_type":"code","execution_count":null,"id":"93182db7","metadata":{},"outputs":[],"source":["%ngs sum(0..10)"]},{"cell_type":"code","execution_count":null,"id":"61de49c7","metadata":{},"outputs":[],"source":[]}],"metadata":{"kernelspec":{"display_name":"Python 3 (ipykernel)","language":"python","name":"python3"},"language_info":{"codemirror_mode":{"name":"ipython","version":3},"file_extension":".py","mimetype":"text\/x-python","name":"python","nbconvert_exporter":"python","pygments_lexer":"ipython3","version":"3.9.7"}},"nbformat":4,"nbformat_minor":5}' > NGS_example.ipynb && chown ${NB_UID} NGS_example.ipynb

USER ${NB_UID}