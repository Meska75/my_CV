from django.db import migrations


def clear_stock_images(apps, schema_editor):
    ServiceCard = apps.get_model('my_cv', 'ServiceCard')
    ServiceCard.objects.filter(static_image__startswith='snapfolio/img/').update(static_image='')


class Migration(migrations.Migration):

    dependencies = [
        ('my_cv', '0007_servicecard'),
    ]

    operations = [
        migrations.RunPython(clear_stock_images, migrations.RunPython.noop),
    ]
