import boto3
from ast import literal_eval


class EC2Error(RuntimeError):
    """ EC2 Exception interface (RuntimeError)

    """
    pass


class TerminationError(EC2Error):
    """ EC2 Instance Termination status fail

    """
    pass


class EC2:
    """ EC2 Client Class

    """

    def __init__(self, region_name: str=None, profile_name: str=None):
        # default region us-east-1 virginia
        if region_name is None:
            self._region_name = 'us-east-1'
        else:
            self._region_name = region_name

        if profile_name:
            self._session = boto3.session.Session(region_name=self._region_name, profile_name=profile_name)
        else:
            self._session = boto3.session.Session(region_name=self._region_name)

        self.ec2 = self._session.resource('ec2')
        self.images = ec2.images.all()
        self.instances = []

    @property
    def region(self):
        return self._region_name

    @property
    def profile_name(self):
        return self._session.profile_name

    def list(self, filters: dict = None, state: str = None, exclude: str = None) -> list:
        """ List instances within a specific state, filter or exclude item

        :type state: str
        :param state: possible states: running, stopped
        :param filters: a dict string literal_eval {'Name': 'v1', 'Values': 'v2'}
        :param exclude: list of excluded id's
        :return: collection of ec2 instances
        :rtype: list
        """
        date_format = '%Y-%m-%d %H:%M:%S'
        self.instances = self.ec2.instances.all()

        # TOREMOVE
        def __all_instances():
            # all instances without filtering
            self.instances = [
                {
                    'InstanceId': instance.id,
                    'State': instance.state['Name'],
                    'Type': instance.instance_type,
                    'VpcId': instance.vpc_id,
                    'KeyName': instance.key_name,
                    'Tags': instance.tags,
                    'StartedAt': instance.launch_time.strftime(date_format)
                }
                for instance in self.instances
            ]

        if state:
            try:
                self.instances = self.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': [state]}])
            except IOError as e:
                raise EC2Error('Error listing instances by state {0} {1}'.format(state, e))

        if filters:
            # convert string into dict
            filters = literal_eval(filters)
            try:
                if not self.instances:
                    self.instances = self.ec2.instances.all()

                self.instances = self.instances.filter(Filters=[{'Name': filters['Name'], 'Values': filters['Values']}])
            except IOError as e:
                raise EC2Error('Error listing instances with filters {0} {1}'.format(filters, e))

        if exclude:
            instances = []
            for i in self.instances:
                if i.id not in exclude:
                    instances.append(i)
            return [
                {
                    'InstanceId': instance.id,
                    'State': instance.state['Name'],
                    'Type': instance.instance_type,
                    'VpcId': instance.vpc_id,
                    'KeyName': instance.key_name,
                    'Tags': instance.tags,
                    'StartedAt': instance.launch_time.strftime(date_format)
                }
                for instance in instances
            ]
        else:
            return [
                {
                    'InstanceId': instance.id,
                    'State': instance.state['Name'],
                    'Type': instance.instance_type,
                    'VpcId': instance.vpc_id,
                    'KeyName': instance.key_name,
                    'Tags': instance.tags,
                    'StartedAt': instance.launch_time.strftime(date_format)
                }
                for instance in self.instances
            ]

    def describe(self):
        pass

    def start(self):
        pass

    def stop(self, ids: list) -> str:
        """ Stop instances based on a list of ids

        :param ids:
        :rtype: str
        :return: list
        """
        # If no ids are passed raise Nothing to do
        if 'None' in ids:
            raise EC2Error('Nothing to do. Need IDS! Arrgh!!!')

        try:
            status = self.ec2.instances.filter(InstanceIds=ids).stop()
            return status
        except IOError as e:
            raise EC2Error('Error stopping EC2 Instances {}'.format(e))

    def terminate(self, ids: list, exclude: list = None) -> str:
        """ Terminate instances based on a list of ids

        :param exclude:
        :param ids:
        :return:
        :rtype: str
        """
        if exclude is None:
            try:

                status = self.ec2.instances.filter(InstanceIds=ids).terminate()
                return "Terminated status: {0}, instances:\n {1}".format(ids, status)
            except IOError as e:
                raise TerminationError('Error terminating EC2 Instances {}'.format(e))
        else:
            #filtered_ids = list(set(ids) - set(exclude))
            try:
                # status = self.ec2.instances.filter(InstanceIds=filtered_ids).terminate()
                status = self.instances = self.ec2.instances.filter(
                            Filters=[
                                {'Name': 'instance-state-name', 'Values': [state]}
                            ]
                        )
                return "Terminated status: {0}, instances:\n {1}".format(filtered_ids, status)
            except IOError as e:
                raise TerminationError('Error terminating EC2 Instances {}'.format(e))


if __name__ == '__main__':
    ec2 = EC2()
    print('stopped')
    print(ec2.list(state='stopped'))
    print('running')
    running = ec2.list(state='running')
    print(ec2.list(state='running'))
    print(running)

    # stop_result = ec2.stop(ids=['1asf1323'])
    # terminate_result = ec2.terminate(ids=['1asf1323'])
    # print('Instance list: {0}\n Stop: {1}\n Terminate: {2}'.format(instance_list, stop_result, terminate_result))

