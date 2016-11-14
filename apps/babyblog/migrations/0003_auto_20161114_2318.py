# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('babyblog', '0002_auto_20161114_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=70)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tweet_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tweet', to='babyblog.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='message_user',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]