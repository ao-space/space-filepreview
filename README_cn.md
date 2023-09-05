# space-filepreview

[English](./README.md) | 简体中文

## 简介

space-filepreview 是一个异步文件预览与缩略图服务

它可以与 aospace aofs 配合，将上传到傲空间的文件异步生成缩略图或预览文件

## 功能介绍

异步从 redis 中读取上传文件的事件，并根据事件内容，对相应文件进行处理，生成缩略图或预览文档

预览文件主要支持

- office 文档
- pdf 文档
- txt 等文本文档

图片缩略图支持的格式与[preview-generator](https://github.com/algoo/preview-generator) 保持一致

包括常见的，jpg，png，webp，gif, bmp，heic等

**部分安卓手机的 10bit heic 格式暂不支持**

## 构建

### 依赖组件
<https://github.com/algoo/preview-generator>

### 安装preview-generator

- Python >= 3.5

**以Debian GNU/Linux 11 为例**

```shell
apt-get install poppler-utils qpdf libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev ffmpeg
```

### 安装其他依赖

```shell
pip install -r requirements.txt
```

### 镜像构建

进入项目根目录，运行

```shell
docker build -t local/space-filepreview:{tag} . 
````

## 运行

```shell
python main.py
```

## 注意事项

环境变量

      REDIS_HOST: aospace-redis
      REDIS_PORT: 6379
      REDIS_PASSWORD: "placeholder_mysecretpassword"
      BUCKET_SOURCE: "eulixspace-files"
      BUCKET_TARGET: "eulixspace-files-processed"
      ROOT_DATA_DIR: "/data/"
      LIBREOFFICE_PROCESS_TIMEOUT: 900
      DEBUG_MODE: 1

## 贡献指南

我们非常欢迎对本项目进行贡献。以下是一些指导原则和建议，希望能够帮助您参与到项目中来。

[贡献指南](https://github.com/ao-space/ao.space/blob/dev/docs/cn/contribution-guidelines.md)

## 联系我们

- 邮箱：<developer@ao.space>
- [官方网站](https://ao.space)
- [讨论组](https://slack.ao.space)

## 感谢您的贡献

最后，感谢您对本项目的贡献。我们欢迎各种形式的贡献，包括但不限于代码贡献、问题报告、功能请求、文档编写等。我们相信在您的帮助下，本项目会变得更加完善和强大。
