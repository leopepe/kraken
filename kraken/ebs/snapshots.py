import boto3
# from kraken import ec2
import re


class SnapShots:

    def __init__(self) -> object:
        self.ec2 = boto3.resource('ec2')
        iam = boto3.resource('iam')
        self.account_id = iam.CurrentUser().arn.split(':')[4]
        self.my_images = self.ec2.images.filter(Owners=[self.account_id])

    def main(self):
        for snapshot in self.ec2.snapshots.filter(OwnerIds=[self.account_id]):
            r = re.match(r".*for (ami-.*) from.*", snapshot.description)
            if r:
                if r.groups()[0] not in self.my_images:
                    # snapshot.delete()
                    print('snapshot.delete()', snapshot)


if __name__ == '__main__':
    snap = SnapShots()
    snap.main()
