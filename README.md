# Kraken

An AWS CLI for destructive operations. Kraken can terminate all ec2 instances, available ebs volumes and old snapshots.

**Author: Leonardo Pepe de Freitas**

## Install

To perform a virtualenv installation, it means, the kraken cli will be installed inside $PWD/venv directory, run the followin command:

```
$ make all
```

If you are inttent to only generate a virtualenv with all package requirements:

```
$ make virtualenv
```

The recommend format is by using docker. To create a docker image run:

```
$ make docker
```

After the docker image creation the container can be started.

## Usage

```
$ docker run \
  --rm \
  -e "AWS_ACCESS_KEY_ID=BLABLABLA" \
  -e "AWS_SECRET_KE=TRALALA" \
  -e "AWS_DEFAULT_REGION=us-east-1" \
  -it \
  kraken:1.2.0 \
  python3 -m kraken ec2 ls --state=stopped 
```

