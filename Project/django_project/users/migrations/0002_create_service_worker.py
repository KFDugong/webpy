from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Product
from reviews.models import Comment


def create_servicekraft_group(apps, schema_editor):
    servicekraft_group, created = Group.objects.get_or_create(name="Servicekraft")
    
    # Retrieve or create the permissions for the Product model
    product_content_type = ContentType.objects.get_for_model(Product)
    
    add_product_permission, created = Permission.objects.get_or_create(
        codename="add_product",
        content_type=product_content_type,
    )
    change_product_permission, created = Permission.objects.get_or_create(
        codename="change_product",
        content_type=product_content_type,
    )
    delete_product_permission, created = Permission.objects.get_or_create(
        codename="delete_product",
        content_type=product_content_type,
    )

    servicekraft_group.permissions.add(
        add_product_permission, change_product_permission, delete_product_permission
    )

    # Retrieve or create the permissions for the Comment model
    comment_content_type = ContentType.objects.get_for_model(Comment)
    
    change_comment_permission, created = Permission.objects.get_or_create(
        codename="change_comment",
        content_type=comment_content_type,
    )
    delete_comment_permission, created = Permission.objects.get_or_create(
        codename="delete_comment",
        content_type=comment_content_type,
    )

    servicekraft_group.permissions.add(
        change_comment_permission, delete_comment_permission
    )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_servicekraft_group),
    ]
