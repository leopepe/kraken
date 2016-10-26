import boto3
import datetime
from kraken import ec2

"""
TODO:
 - List all AMI older than X Months
 - List all AMI by TAG
"""


class AMIError(RuntimeError):
    """ AMI generic ERROR

    """
    pass


class DeregisterError(AMIError):
    """ Could not deregister image

    """


class AMI:

    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        __iam = boto3.resource('iam')
        __account_id = __iam.CurrentUser().arn.split(':')[4]
        __instances = self.ec2.instances.all()
        self.my_images = self.ec2.images.filter(Owners=[__account_id])
        #
        self.today = datetime.datetime.now()
        #
        self.running_images_ids = [instance.image_id for instance in __instances]
        self.my_images_ids = [image.image_id for image in self.my_images]
        self.unused_images = set(self.my_images_ids) - set(self.running_images_ids)
        self.inuse_images = set(self.my_images_ids) & set(self.running_images_ids)
        self.project_img_dict = self.images_by_project()

    def list_unused_images(self) -> set:
        return self.unused_images

    def list_inuse_images(self) -> set:
        return self.inuse_images

    def __existing_projects(self) -> set:
        """ ami by project
        :rtype: set
        :return: available projects set
        """
        projects = set()
        for image_id in self.unused_images:
            for tag in self.ec2.Image(image_id).tags:
                if tag['Key'] == 'project':
                    projects.add(tag['Value'])

        return projects

    def timedelta_days_ago(self, days) -> datetime:
        return self.today - datetime.timedelta(days=days)

    def deregister_image_by_age(self, days_old: int=90):
        """ deregister images older then int days_old

        :param days_old: int
        :return: void()
        """
        for image_id in self.unused_images:
            created_date = datetime.datetime.strptime(
                self.ec2.Image(image_id).creation_date, "%Y-%m-%dT%H:%M:%S.000Z"
            )
            if created_date > self.timedelta_days_ago(days=days_old):
                try:
                    # self.ec2.Image(id).deregister()
                    print('AMIs older then {0} days: {1} not in use'.format(days_old, image_id))
                except IOError as e:
                    raise DeregisterError('Could not deregister image: {}'.format(e))

    def images_by_project(self, project) -> dict:
        images = {}
        to_delete = []
        # if project is not set traverse all images[tag] = project
        if not project:
            for project in self.__existing_projects():
                to_delete = []
                for img_id in self.unused_images:
                    [to_delete.append(img_id) for item in self.ec2.Image(img_id).tags if item['Key'] == 'project' and item['Value'] == project]:

                images[project] = to_delete
        else:
           for img_id in self.unused_images:
                [to_delete.append(img_id) for item in self.ec2.Image(img_id).tags if item['Key'] == 'project' and item['Value'] == project]
            images[project] = to_delete
        try:
            if images:
                return images
        except NotImplementedError as e:
            raise('Your images does not has the tag \'project\' on it. {}'.format(e))

    def deregister_image_by_count(self, filters: list=None, keep_last: int=3):
        if filters is None:
            filters = [{'Name': 'tag:project', 'Values': list(self.__existing_projects())}]

        for image in self.my_images.filter(Filters=filters):
            print(image)

        # return candidate


if __name__ == '__main__':
    ami = AMI()
    ami.list_unused_images()
    # ami.deregister_image_by_age(days_old=90)
    ami.deregister_image_by_count(keep_last=3)

