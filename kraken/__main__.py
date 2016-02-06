import click
from kraken import ec2
from kraken import ebs


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
@click.option('--state', '-s', nargs=1, default='stopped')
@click.option('--filters', '-f', multiple=True)
def ec2_ls(state, debug, filters):
    """ List EC2 instances

        format: [{'InstanceId': 'i-88dea039', 'State': 'stopped', 'Type': 't2.micro', 'StartedAt': '2015-12-31 21:58:10', 'VpcId': 'vpc-b0d602d4'}]

    """
    # setting instances
    instances = ec2_client.list(state=state)

    if debug:
        click.echo('[DEBUG]')
        click.echo('State: {0], Debug: {1}'.format(state, debug))

    if filters:
        instances = ec2_client.list(state=state, filters=filters)
        click.echo(instances)
    else:
        click.echo(instances)


@ec2.command('rm')
@click.option('--all', '-a', type=bool, default=False, help='Delete all stopped instances')
@click.option('--ids', help='List of running instances ids to be deleted')
def ec2_rm(ids, all):
    """ Terminate ec2 instances.

    :param ids:
    """
    if all:
        ids = ec2_client.list(state='stopped')
        ec2_client.terminate(ids=ids)

    ec2_client.terminate(ids=ids)


@ec2.command('stop')
@click.option('--ids', type=list, help='List of running instances ids to be stopped')
@click.option('--all', type=bool, default=False, help='Stop all instances running')
def ec2_stop(ids, all):
    """ Stop ec2 instance

    :param:
    :rtype:
    :return:
    """
    if all:
        pass
    else:
        click.echo('Stopping ids: {}'.format(ids))
        ec2_client.stop(ids=ids)


@cli.group()
def ebs():
    """ Manages EBS resources. """


@ebs.command('describe')
@click.argument('ids')
def ebs_describe(ids):
    """ Describe ebs volumes
    :param: ids:
    """
    ebs_client.get_volumes(ids=ids)


@ebs.command('ls')
@click.option('--available', default=False)
def ebs_ls(available):
    """ List EBS volumes. """
    if available:
        click.echo('ebs ls experimental')
        return [volumes for volumes in ebs_client.get_available_volumes()]
    else:
        click.echo('listing all volumes')
        return [volumes for volumes in ebs_client.get_all_volumes()]


@ebs.command('rm')
@click.option('--state', default='available')
def ebs_rm(state):
    available_volumes = ebs_client.get_available_volumes()
    deleted_volumes = []
    candidate_volumes = [
        volume
        for volume in available_volumes
        if ebs_client.is_candidate(volume.volume_id)
    ]
    # delete the unused volumes
    # WARNING -- THIS DELETES DATA
    for candidate in candidate_volumes:
        # logging
        candidate.delete()
        deleted_volumes.append(candidate)


if __name__ == '__main__':
    cli()
