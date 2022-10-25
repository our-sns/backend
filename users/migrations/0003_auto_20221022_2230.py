# Generated by Django 3.2.13 on 2022-10-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20221022_2230'),
        ('users', '0002_alter_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_comment',
            field=models.ManyToManyField(related_name='user_like_comment', through='comments.CommentLike', to='comments.Comment', verbose_name='좋아요 누른 댓글'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='프로필 이름', max_length=20, verbose_name='프로필 이름'),
        ),
    ]
