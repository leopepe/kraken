import boto3


class EC2Error(RuntimeError):
    """ EC2 Exception interface (RuntimeError)

    """
    pass


class EC2:
    """ EC2 Client Class

    """

    def __init__(self, region_name=None, profile_name=None):
        # default region us-east-1 virginia
        if region_name is None:
            self._region_name = 'us-east-1'
        else:
            self._region_name = region_name

        if profile_name is not None:
            self._session = boto3.session.Session(region_name=self._region_name, profile_name=profile_name)
        else:
            self._session = boto3.session.Session(region_name=self._region_name)

        self.ec2 = self._session.resource('ec2')
        self.instances = []

    @property
    def region(self):
        return self._region_name

    @property
    def profile_name(self):
        return self._session.profile_name

    def list(self, filters: list = None, state: str = '') -> list:
        """ List instances within a specific state

        :type state: str
        :param state: possible states: running, stopped
        :return: collection of ec2 instances
        :rtype: list
        """
        date_format = '%Y-%m-%d %H:%M:%S'

        try:
            self.instances = self.ec2.instances.filter(
                Filters=[
                    {'Name': 'instance-state-name', 'Values': [state]}
                ]
            )
            if filters:
                print(filters)
                filtered_list = []
                for d in self.instances:
                    print(d)
                    for k, v in d.items():
                        print(k, v)
                        if k in filters:
                            filtered_list.append(v)
                return filtered_list

            # use list comprehension to generate a collection of instances
            return [
                {
                    'InstanceId': instance.id,
                    'State': instance.state['Name'],
                    'Type': instance.instance_type,
                    'VpcId': instance.vpc_id,
                    'StartedAt': instance.launch_time.strftime(date_format)
                }
                for instance in self.instances
            ]
        except IOError as e:
            raise EC2Error('Error accessing instances {}'.format(e))

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
        try:
            status = self.ec2.instances.filter(InstanceIds=ids).stop()
            return status
        except IOError as e:
            raise EC2Error('Error stopping EC2 Instances {}'.format(e))

    def terminate(self, ids: list) -> str:
        """ Terminate instances based on a list of ids

        :param ids:
        :return:
        :rtype: str
        """
        try:
            status = self.ec2.instances.filter(InstanceIds=ids).terminate()
            return "Terminated status: {0}, instances:\n {1}".format(ids, status)
        except IOError as e:
            raise EC2Error('Error terminating EC2 Instances {}'.format(e))


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

