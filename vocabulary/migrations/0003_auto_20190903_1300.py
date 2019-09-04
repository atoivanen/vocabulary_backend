# Generated by Django 2.1.7 on 2019-09-03 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocabulary', '0002_auto_20190620_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='pronunciation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='source_lang',
            field=models.CharField(choices=[('fr', 'French'), ('fi', 'Finnish'), ('it', 'Italian'), ('en', 'English')], max_length=2, verbose_name='Source language'),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='target_lang',
            field=models.CharField(choices=[('fr', 'French'), ('fi', 'Finnish'), ('it', 'Italian'), ('en', 'English')], max_length=2, verbose_name='Target language'),
        ),
        migrations.AlterField(
            model_name='word',
            name='source_lang',
            field=models.CharField(choices=[('fr', 'French'), ('fi', 'Finnish'), ('it', 'Italian'), ('en', 'English')], max_length=2, verbose_name='Source language'),
        ),
        migrations.AlterField(
            model_name='word',
            name='target_lang',
            field=models.CharField(choices=[('fr', 'French'), ('fi', 'Finnish'), ('it', 'Italian'), ('en', 'English')], max_length=2, verbose_name='Target language'),
        ),
    ]
