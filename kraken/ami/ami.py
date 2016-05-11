from kraken import ec2


def main():
    instances = ec2.instances.all()
    my_images = ec2.images.filter(Owners=["my-account-id"))

    # anything that's running or stopped we want to keep the AMI
    good_images = set([instance.image_id for instance in ec2.instances.all()])

    # build a dictionary of all the images that aren't in good_images
    my_images_dict = {image.id: image for image in my_images if image.id not in good_images}
    # now lets deregister all the AMIs older than two weeks
    for image in image.values():
        created_date = datetime.strptime(
            image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
        if created_date < two_weeks_ago:
             image.deregister()

if __name__ == '__main__':
    main()
