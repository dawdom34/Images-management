from users.models import AccountTier, ThumbnailSizes


def run():
    """
    Create build in account tiers (Basic, Premium, Enterprise)
    """
    # Create default thumbnail sizes objects
    ThumbnailSizes.objects.create(size=200)
    ThumbnailSizes.objects.create(size=400)

    size_200 = ThumbnailSizes.objects.get(size=200)
    size_400 = ThumbnailSizes.objects.get(size=400)

    # Create Basic tier
    basic = AccountTier.objects.create(name='Basic', original_file=False, expiring_links=False)
    basic.thumbnail_size.add(size_200)

    # Create Premium tier
    premium = AccountTier.objects.create(name='Premium', original_file=True, expiring_links=False)
    premium.thumbnail_size.add(size_200)
    premium.thumbnail_size.add(size_400)

    # Create Enterprise tier
    ent = AccountTier.objects.create(name='Enterprise', original_file=True, expiring_links=True)
    ent.thumbnail_size.add(size_200)
    ent.thumbnail_size.add(size_400)
