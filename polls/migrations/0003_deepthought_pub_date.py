# Generated by Django 4.1.1 on 2022-09-28 13:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0002_deepthought"),
    ]

    operations = [
        migrations.AddField(
            model_name="deepthought",
            name="pub_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="date published"
            ),
            preserve_default=False,
        ),
    ]