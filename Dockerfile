# Copyright (c) 2022 Institute of Software, Chinese Academy of Sciences (ISCAS)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM debian:experimental

ENV LANG C.UTF-8

ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		ca-certificates \
		netbase \
		tzdata \
                gcc g++ python3 python3-pip python3-full python3-dev \
	; \
	rm -rf /var/lib/apt/lists/*
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime; \
        echo ${TZ} > /etc/timezone; \
        dpkg-reconfigure --frontend noninteractive tzdata; \
        rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install --no-install-recommends \
        apt-transport-https ca-certificates poppler-utils qpdf \
        libfile-mimeinfo-perl libimage-exiftool-perl ghostscript \
        libsecret-1-0 zlib1g-dev libjpeg-dev ffmpeg python3-magic \
        libmagickwand-dev imagemagick -y \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/eulixspace-filepreview

COPY . /opt/eulixspace-filepreview

RUN pip3 install -r /opt/eulixspace-filepreview/requirements.txt --break-system-packages

ENTRYPOINT ["python3","main.py"]
