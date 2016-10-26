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

### Exemples

Montando o .aws com as credenciais de acesso a AWS

```shell
$ docker run --rm -v $HOME/.aws:/root/.aws -it kraken:latest ec2 rm --stopped
Termination result: Terminated status: ['i-7b7cc1e1'], instances:
 [{'TerminatingInstances': [{'CurrentState': {'Name': 'terminated', 'Code': 48}, 'InstanceId': 'i-7b7cc1e1', 'PreviousState': {'Name': 'stopped', 'Code': 80}}], 'ResponseMetadata': {'RequestId': '7c5d77bd-0e83-4c72-9520-b801ef0ab395', 'HTTPStatusCode': 200}}] [instance was stopped]

$ docker run --rm -v $HOME/.aws:/root/.aws -it kraken:latest ec2 stop --all
Stop result: [{'StoppingInstances': [{'CurrentState': {'Code': 64, 'Name': 'stopping'}, 'InstanceId': 'i-b77fc22d', 'PreviousState': {'Code': 16, 'Name': 'running'}}], 'ResponseMetadata': {'RequestId': 'e8dd11f1-1189-42b4-b28d-0f9a77cf6184', 'HTTPStatusCode': 200}}]

$ docker run --rm -v $HOME/.aws:/root/.aws -it kraken:latest ec2 rm --stopped
Termination result: Terminated status: ['i-b77fc22d'], instances:
 [{'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '99ac1396-7a93-436e-895b-38f851b24f0c'}, 'TerminatingInstances': [{'PreviousState': {'Code': 80, 'Name': 'stopped'}, 'InstanceId': 'i-b77fc22d', 'CurrentState': {'Code': 48, 'Name': 'terminated'}}]}] [instance was stopped]
```


### TODO

- List / Destroy by tag: # ec2.filter(Filters=[{'Name': 'tag:Name', 'Values': [tag]}])
