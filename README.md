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

### List stopped ec2 instances:

```
$ docker run \
  --rm \
  -e "AWS_ACCESS_KEY_ID=BLABLABLA" \
  -e "AWS_SECRET_KE=TRALALA" \
  -e "AWS_DEFAULT_REGION=us-east-1" \
  -it \
  kraken:1.2.0 \
  ec2 ls --state=stopped
```

### General help:

```
$ docker run \
  --rm \
  -e "AWS_ACCESS_KEY_ID=BLABLABLA" \
  -e "AWS_SECRET_KE=TRALALA" \
  -e "AWS_DEFAULT_REGION=us-east-1" \
  -it \
  kraken:1.2.0 --help
```

### Sub-Command and command help:

```
$ docker run \
  --rm \
  -e "AWS_ACCESS_KEY_ID=BLABLABLA" \
  -e "AWS_SECRET_KE=TRALALA" \
  -e "AWS_DEFAULT_REGION=us-east-1" \
  -it \
  kraken:1.2.0 ec2 --help
```

### TODO

- List / Destroy by tag: # ec2.filter(Filters=[{'Name': 'tag:Name', 'Values': [tag]}])