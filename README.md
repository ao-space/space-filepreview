# space-filepreview

English | [简体中文](./README_cn.md)

## Introduce

space-filepreview is an asynchronous file preview and thumbnail service.

It works with aospace aofs to asynchronously generate thumbnails or previews of files uploaded to AOspace.

## Feature

Read the event of uploading a file from redis,
and according to the content of the event,
process the corresponding file to generate a thumbnail or preview document

The preview file mainly supports

- office documents
- pdf documents
- txt and other text documents

Image thumbnails support formats consistent with [preview-generator](https://github.com/algoo/preview-generator)

Including common, jpg, png, webp, gif, bmp, heic and so on.

**10bit heic format is not supported by some Android phones at the moment**.

## Build

### Dependent component

[preview-generator](https://github.com/algoo/preview-generator)

### install preview-generator

- Python >= 3.5

**Take Debian GNU/Linux 11 for example.**

```shell
apt-get install poppler-utils qpdf libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev ffmpeg
```

### install other dependency

```shell
pip install -r requirements.txt
```

### build image

go into project root path,and run

```shell
docker build -t local/space-filepreview:{tag} . 
````

## Run

```shell
python main.py
```

## Notes

Environment

      REDIS_HOST: aospace-redis
      REDIS_PORT: 6379
      REDIS_PASSWORD: "placeholder_mysecretpassword"
      BUCKET_SOURCE: "eulixspace-files"
      BUCKET_TARGET: "eulixspace-files-processed"
      ROOT_DATA_DIR: "/data/"
      LIBREOFFICE_PROCESS_TIMEOUT: 900
      DEBUG_MODE: 1

## Contribution Guidelines

Contributions to this project are very welcome. Here are some guidelines and suggestions to help you get involved in the project.

[Contribution Guidelines](https://github.com/ao-space/ao.space/blob/dev/docs/en/contribution-guidelines.md)

## Contact us

- Email: <developer@ao.space>
- [Official Website](https://ao.space)
- [Discussion group](https://slack.ao.space)

## Thanks for your contribution

Finally, thank you for your contribution to this project. We welcome contributions in all forms, including but not limited to code contributions, issue reports, feature requests, documentation writing, etc. We believe that with your help, this project will become more perfect and stronger.
