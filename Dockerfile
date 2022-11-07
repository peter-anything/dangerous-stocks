FROM python:3.7-buster

COPY requirements.txt .

RUN sed -i 's#http://deb.debian.org#https://mirrors.163.com#g' /etc/apt/sources.list

RUN pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --upgrade pip  && \
    pip --default-timeout=200 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn


ADD *.py /codes/
ADD stock/ /codes/stock/
ADD static /codes/static/
ADD start.sh /codes/

WORKDIR /codes

CMD ["/bin/bash", "start.sh"]
