import click
from .ec2 import ec2
from .ebs import ebs
import json

ec2_client = ec2.EC2()
ebs_client = ebs.EBS()


@click.group()
@click.version_option()
def cli():
    """ Kraken demo

    Kraken is a destructive EC2 client.
    """


@cli.group()
def ec2():
    """ EC2 resources client. """


@ec2.command('ls')
@click.option('--debug', '-d', help='Enables debug mode')
@click.option('--state', '-s', nargs=1, default=None)
@click.option('--filters', '-f', multiple=False, type=str, default=None)
@click.option('--exclude', '-e', multiple=False, type=str, default=None)
def ec2_ls(state, debug, filters, exclude):
    """ List EC2 instances

        format: [{'InstanceId': 'i-88dea039', 'State': 'stopped', 'Type': 't2.micro', 'StartedAt': '2015-12-31 21:58:10', 'VpcId': 'vpc-b0d602d4'}]
    :param state:
    :param debug:
    :param filters:
    :param exclude:
    """
    # setting instances
    instances = ec2_client.list(state=state, exclude=exclude, filters=filters)
    click.echo(json.dumps(instances, ensure_ascii=False, indent=2))


@ec2.command('rm')
@click.option('--ids', '-i', type=str, help='List of running instances ids to be terminated')
@click.option('--running/--stopped', default=False, help='Terminate all instances running')
@click.option('--exclude', '-e', default=False, type=str, help='The list of ids must be separated by one white space')
def ec2_rm(ids, running, exclude):
    """ Terminate ec2 instances.

    :param ids: list of instance ids to terminated
    :param exclude
    :param running
    """
    if running:
        instances = ec2_client.list(state='running', exclude=exclude)
        ids = [
            instance['InstanceId']
            for instance in instances
        ]
        result = ec2_client.terminate(ids) + ' [instance was running]'

    elif ids:
        result = ec2_client.terminate(ids) + ' [instance ids terminated]'

    else:
        instances = ec2_client.list(state='stopped', exclude=exclude)
        ids = [
            instance['InstanceId']
            for instance in instances
        ]
        result = ec2_client.terminate(ids) + ' [instance was stopped]'

    click.echo('Termination result: {}'.format(result))


@ec2.command('stop')
@click.option('--ids', '-i', type=str, help='List of running instances ids to be stopped')
@click.option('--all/--not-all', default=False, help='Stop all instances running')
@click.option('--exclude', '-e', default=False, type=str, help='The list of ids must be separated by one white space')
def ec2_stop(ids, all, exclude):
    """ Stop ec2 instance

    :param ids
    :param all
    :param exclude: list of excluded ids
    :rtype str
    :return String containing the result of the instances stop:
    """
    if ids:
        result = ec2_client.stop(ids)
        click.echo('Stop result:\n {}'.format(result))
    else:
        instances = ec2_client.list(state='running', exclude=exclude)
        ids = [
            instance['InstanceId']
            for instance in instances
        ]
        result = ec2_client.stop(ids)
        click.echo('Stop result: {}'.format(result))


@cli.group()
def ebs():
    """ Manages EBS resources. """


@ebs.command('describe')
@click.argument('ids')
def ebs_describe(ids):
    """ Describe ebs volumes
    :param ids
    """
    ebs_client.get_volume_by_id(ids=ids)


@ebs.command('ls')
@click.option('--available/--all', default=False)
def ebs_ls(available):
    """ List EBS volumes.
    :param available
    """
    if available:
        available = ebs_client.get_available_volumes()
        click.echo('All available volumes: {}'.format(available))
    else:
        all_volumes = ebs_client.get_all_volumes()
        click.echo('All volumes: {}'.format(all_volumes))


@ebs.command('rm')
@click.option('--available/--candidate', default=False)
def ebs_rm(available):
    """ Destroy EBS volumes. Default state = available """
    if available:
        click.echo('Terminating volumes: {}'.format(ebs_client.get_available_volumes()))
        ebs_client.terminate_available()
    else:
        terminated = ebs_client.terminate_candidates()
        if terminated:
            click.echo('Ye ebs volumes deleted!')
        else:
            click.echo('ARR! Error deleting volumes!')


if __name__ == '__main__':
    cli()
