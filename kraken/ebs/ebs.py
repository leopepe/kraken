import boto3
from datetime import datetime, timedelta


class EBSError(RuntimeError):
    """ EBS Exception interface (RuntimeError)

    """
    pass


class EBS:

    def __init__(self):
        region = "us-east-1"
        two_weeks = timedelta(days=14)
        self.ec2 = boto3.resource("ec2", region_name=region)
        self.cloud_watch = boto3.client("cloudwatch", region_name=region)
        self.today = datetime.now() + timedelta(days=1)  # today + 1 because we want all of today
        self.start_date = self.today - two_weeks
        self.all_volumes = self.ec2.volumes.all()

    def get_volume_by_id(self, ids: list):
        """

        :param ids:
        :return: list of volumes_info
        :rtype: list
        """
        volumes_info = self.ec2.Volume(ids)
        return volumes_info

    def get_all_volumes(self):
        ids = [volume.id for volume in self.ec2.volumes.all()]
        return ids

    def get_metrics(self, volume_id):
        """ Get volume idle time on an individual volume over `start_date`
           to today

        :parameter: volume_id
        :rtype: object
        :returns: metrics
        """
        metrics = self.cloud_watch.get_metric_statistics(
            Namespace='AWS/EBS',
            MetricName='VolumeIdleTime',
            Dimensions=[{'Name': 'VolumeId', 'Value': volume_id}],
            Period=3600,  # every hour
            StartTime=self.start_date,
            EndTime=self.today,
            Statistics=['Minimum'],
            Unit='Seconds'
        )
        return metrics['Datapoints']

    def terminate_candidates(self):

        def __is_candidate(volume_id):
            """Make sure the volume has not been used in the past two weeks"""
            metrics = self.get_metrics(volume_id)
            if len(metrics):
                for metric in metrics:
                    # idle time is 5 minute interval aggregate so we use
                    # 299 seconds to test if we're lower than that
                    if float(metric['Minimum']) < float(299):
                        print('volume metric is lower then 299')
                        return False
            # if the volume had no metrics lower than 299 it's probably not
            # actually being used for anything so we can include it as
            # a candidate for deletion
            return True

        available_volumes = self.get_available_volumes()
        candidate_volumes = [
            volume
            for volume in available_volumes
            if __is_candidate(volume.volume_id)
        ]
        # delete the unused volumes
        # WARNING -- THIS DELETES DATA
        for candidate in candidate_volumes:
            print('deleting {}'.format(candidate))
            candidate.delete()

        """
        candidates = self.get_candidate_volumes()
        try:
            for candidate in candidates:
                candidate.delete()
            return True
        except IOError as e:
                raise EBSError('ARR! Error destroying ebs volumes {}'.format(e))
        """

    def get_available_volumes(self):
        available_volumes = self.ec2.volumes.filter(
                Filters=[{'Name': 'status', 'Values': ['available']}]
            )

        return available_volumes

    def terminate_available(self):
        try:
            for volume in self.get_available_volumes():
                # volume.delete()
                volume.delete()
                # print(volume)
        except IOError as e:
            raise EBSError('Error deleting volume.s'.format(e))


def main():
    ebs = EBS()
    # Test methods
    available_volumes = ebs.get_available_volumes()
    print('get_available_volumes(): {}'.format(available_volumes))

    all_volumes = ebs.get_all_volumes()
    print('get_all_volumes(): {}'.format(all_volumes))

    volumes_ids = ebs.get_volume_by_id(all_volumes)
    print('Volumes IDS {}'.format(volumes_ids))

    metrics = [ebs.get_metrics(v) for v in all_volumes]
    print('get_metrics: {}'.format(metrics))
    #
    # Terminate metric candidates
    # ebs.terminate_candidates()
    # Terminate all available
    # ebs.terminate_available()


if __name__ == '__main__':
    main()
