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

    def get_volumes(self, ids: list):
        """

        :param ids:
        :return: list of volumes_info
        :rtype: list
        """
        volumes_info = self.ec2.Volume(ids=ids)
        return volumes_info

    def get_all_volumes(self):
        volumes = [volume.id for volume in self.ec2.volumes.all()]
        return volumes

    def get_metrics(self, volume_id):
        """ Get volume idle time on an individual volume over `start_date`
           to today

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

    def is_candidate(self, volume_id):
        """Make sure the volume has not been used in the past two weeks"""
        metrics = self.get_metrics(volume_id)
        if len(metrics):
            for metric in metrics:
                # idle time is 5 minute interval aggregate so we use
                # 299 seconds to test if we're lower than that
                if metric['Minimum'] < 299:
                    return False
        # if the volume had no metrics lower than 299 it's probably not
        # actually being used for anything so we can include it as
        # a candidate for deletion
        return True

    def get_candidate_volumes(self):

        def __available_volumes():
            a = self.ec2.volumes.filter(
                Filters=[{'Name': 'status', 'Values': ['available']}]
            )
            return a

        available_volumes = __available_volumes()
        candidate_volumes = [
            volume
            for volume in available_volumes
            if self.is_candidate(volume.volume_id)
        ]
        return candidate_volumes

    def terminate_candidates(self):
        candidates = self.get_candidate_volumes()
        try:
            for candidate in candidates:
                candidate.delete()
            return True
        except IOError as e:
                raise EBSError('ARR! Error destroying ebs volumes {}'.format(e))

    def get_available_volumes(self):
        available_volumes = self.get_candidate_volumes()
        return available_volumes


def main():
    ebs = EBS()
    # available_volumes_list = [volumes for volumes in ebs.get_available_volumes()]
    available_volumes_list = ebs.get_available_volumes()
    print('available volumes: '.format(available_volumes_list))

    print('all volumes {}'.format(ebs.get_all_volumes()))

    # iterate over volumes list
    # for volume in ebs:
    #     print(volume)
    # metrics = ebs.get_metrics(volume_id='vol-8cc96876')
    # print(metrics)

    # for vol_id in ['vol-8cc96876', 'vol-5ee142a4', 'vol-36c378cc']:
    #     print(ebs.get_metrics(volume_id=vol_id))

    # Test delete volume
    # print('Test delete volumes')
    # available_volumes = ebs.get_available_volumes()
    # candidate_volumes = [
    #     volume
    #     for volume in available_volumes
    #     if ebs.is_candidate(volume.volume_id)
    # ]
    # print('Cadidates: {}'.format(candidate_volumes))
    print('Candidate volumes: {}'.format(ebs.get_candidate_volumes()))
    print('Terminating candidates: {}'.format(ebs.terminate_candidates()))
    # delete the unused volumes
    # WARNING -- THIS DELETES DATA
    # for candidate in candidate_volumes:
    #     candidate.delete()


if __name__ == '__main__':
    main()
