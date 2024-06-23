# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CommentTable(models.Model):
    c_index = models.BigAutoField(primary_key=True)
    c_audience_id = models.BigIntegerField(blank=True, null=True)
    c_like_counts = models.IntegerField(blank=True, null=True)
    c_screen_name = models.CharField(max_length=256, blank=True, null=True)
    c_location = models.CharField(max_length=256, blank=True, null=True)
    c_gender = models.IntegerField(blank=True, null=True)
    c_followers_count = models.IntegerField(blank=True, null=True)
    c_friends_count = models.IntegerField(blank=True, null=True)
    c_statuses_count = models.IntegerField(blank=True, null=True)
    c_text_raw = models.CharField(max_length=2048, blank=True, null=True)
    c_mid = models.ForeignKey('PostTable', models.DO_NOTHING, db_column='c_mid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comment_table'


class PostTable(models.Model):
    p_mid = models.OneToOneField('PostTableAll', models.DO_NOTHING, db_column='p_mid', primary_key=True)
    p_auther = models.CharField(max_length=256, blank=True, null=True)
    p_txt = models.CharField(max_length=6144, blank=True, null=True)
    p_transmit = models.IntegerField(blank=True, null=True)
    p_comment = models.IntegerField(blank=True, null=True)
    p_like = models.IntegerField(blank=True, null=True)
    t_title = models.ForeignKey('TopicTable', models.DO_NOTHING, db_column='t_title', blank=True, null=True)
    p_uid = models.BigIntegerField(blank=True, null=True)
    p_birthday = models.CharField(max_length=256, blank=True, null=True)
    p_constellation = models.CharField(max_length=256, blank=True, null=True)
    p_created_at = models.CharField(max_length=256, blank=True, null=True)
    p_gender = models.IntegerField(blank=True, null=True)
    p_location = models.CharField(max_length=256, blank=True, null=True)
    p_audence_id = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'post_table'


class PostTableAll(models.Model):
    p_mid = models.BigIntegerField(primary_key=True)
    p_auther = models.CharField(max_length=256, blank=True, null=True)
    p_txt = models.CharField(max_length=6144, blank=True, null=True)
    p_transmit = models.IntegerField(blank=True, null=True)
    p_comment = models.IntegerField(blank=True, null=True)
    p_like = models.IntegerField(blank=True, null=True)
    p_title = models.CharField(max_length=256, blank=True, null=True)
    p_uid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'post_table_all'


class TopicTable(models.Model):
    t_title = models.CharField(primary_key=True, max_length=256)
    t_label = models.CharField(max_length=256, blank=True, null=True)
    t_time = models.CharField(max_length=256, blank=True, null=True)
    t_host = models.CharField(max_length=256, blank=True, null=True)
    t_continue = models.IntegerField(blank=True, null=True)
    t_sort = models.IntegerField(blank=True, null=True)
    t_hot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'topic_table'


class TopicTableAll(models.Model):
    t_index = models.AutoField(primary_key=True)
    t_title = models.CharField(max_length=256, blank=True, null=True)
    t_label = models.CharField(max_length=256, blank=True, null=True)
    t_time = models.CharField(max_length=256, blank=True, null=True)
    t_host = models.CharField(max_length=256, blank=True, null=True)
    t_continue = models.IntegerField(blank=True, null=True)
    t_sort = models.IntegerField(blank=True, null=True)
    t_hot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'topic_table_all'

class UserTable(models.Model):
    u_id = models.BigAutoField(primary_key=True)
    u_name = models.CharField(max_length=256)
    u_password = models.CharField(max_length=20)
    u_sex = models.IntegerField(blank=True, null=True)
    u_birth = models.DateField(blank=True, null=True)
    u_txt = models.CharField(max_length=1024, blank=True, null=True)
    u_admin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_table'