# Generated by Django 4.1.4 on 2022-12-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_cloth_created_alter_about_id_alter_brand_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
