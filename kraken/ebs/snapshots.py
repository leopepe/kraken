from kraken import ec2


def main():
    images = ec2.images.all()
    images = [image.id for image in images]

    for snapshot in ec2.snapshots.filter(OwnerIds=["my-account-id"]):
        r = re.match(r".*for (ami-.*) from.*", snapshot.description)
        if r:
            if r.groups()[0] not in images:
                snapshot.delete()


if __name__ == '__main__':
    main()