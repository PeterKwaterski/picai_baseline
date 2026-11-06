FROM joeranbosma/picai_nnunet:latest

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install git+https://github.com/PeterKwaterski/picai_baseline.git@main

ENTRYPOINT $0 $@
