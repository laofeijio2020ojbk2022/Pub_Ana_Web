from django.db import models

# Create your models here.


class CookiesTable(models.Model):
    co_id = models.BigIntegerField(primary_key=True)
    co_cookie = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cookies_table'


class TimeTitleTable(models.Model):
    ti_title = models.CharField(primary_key=True, max_length=256)
    ti_label = models.CharField(max_length=256, blank=True, null=True)
    ti_hot = models.IntegerField(blank=True, null=True)
    ti_time = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'time_title_table'


class TimePostTableAll(models.Model):
    tp_mid = models.BigIntegerField(primary_key=True)
    tp_auther = models.CharField(max_length=256, blank=True, null=True)
    tp_txt = models.CharField(max_length=6144, blank=True, null=True)
    tp_transmit = models.IntegerField(blank=True, null=True)
    tp_comment = models.IntegerField(blank=True, null=True)
    tp_like = models.IntegerField(blank=True, null=True)
    tp_title = models.CharField(max_length=256, blank=True, null=True)
    tp_uid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'time_post_table_all'


class TimePostTable(models.Model):
    tlp_mid = models.BigIntegerField(primary_key=True)
    tlp_auther = models.CharField(max_length=256, blank=True, null=True)
    tlp_txt = models.CharField(max_length=6144, blank=True, null=True)
    tlp_transmit = models.IntegerField(blank=True, null=True)
    tlp_comment = models.IntegerField(blank=True, null=True)
    tlp_like = models.IntegerField(blank=True, null=True)
    tlp_title = models.CharField(max_length=256, blank=True, null=True)
    tlp_uid = models.BigIntegerField(blank=True, null=True)
    tlp_birthday = models.CharField(max_length=256, blank=True, null=True)
    tlp_constellation = models.CharField(max_length=256, blank=True, null=True)
    tlp_created_at = models.CharField(max_length=256, blank=True, null=True)
    tlp_gender = models.IntegerField(blank=True, null=True)
    tlp_location = models.CharField(max_length=256, blank=True, null=True)
    tlp_audence_id = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'time_post_table'


class TimeCommentTable(models.Model):
    tc_index = models.BigAutoField(primary_key=True)
    tc_audience_id = models.BigIntegerField(blank=True, null=True)
    tc_like_counts = models.IntegerField(blank=True, null=True)
    tc_screen_name = models.CharField(max_length=256, blank=True, null=True)
    tc_location = models.CharField(max_length=256, blank=True, null=True)
    tc_gender = models.IntegerField(blank=True, null=True)
    tc_followers_count = models.IntegerField(blank=True, null=True)
    tc_friends_count = models.IntegerField(blank=True, null=True)
    tc_statuses_count = models.IntegerField(blank=True, null=True)
    tc_text_raw = models.CharField(max_length=2048, blank=True, null=True)
    tc_mid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'time_comment_table'
