# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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
        managed = False
        db_table = 'comment_table'


class CookiesTable(models.Model):
    co_id = models.BigIntegerField(primary_key=True)
    co_cookie = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cookies_table'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
        managed = False
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
        managed = False
        db_table = 'post_table_all'


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
        managed = False
        db_table = 'time_comment_table'


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
        managed = False
        db_table = 'time_post_table'


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
        managed = False
        db_table = 'time_post_table_all'


class TimeTitleTable(models.Model):
    ti_title = models.CharField(primary_key=True, max_length=256)
    ti_label = models.CharField(max_length=256, blank=True, null=True)
    ti_hot = models.IntegerField(blank=True, null=True)
    ti_time = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_title_table'


class TopicTable(models.Model):
    t_title = models.CharField(primary_key=True, max_length=256)
    t_label = models.CharField(max_length=256, blank=True, null=True)
    t_time = models.CharField(max_length=256, blank=True, null=True)
    t_host = models.CharField(max_length=256, blank=True, null=True)
    t_continue = models.IntegerField(blank=True, null=True)
    t_sort = models.IntegerField(blank=True, null=True)
    t_hot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'topic_table_all'


class UserTable(models.Model):
    u_id = models.BigAutoField(primary_key=True)
    u_name = models.CharField(unique=True, max_length=256)
    u_password = models.CharField(max_length=20)
    u_sex = models.IntegerField(blank=True, null=True)
    u_birth = models.DateField(blank=True, null=True)
    u_txt = models.CharField(max_length=1024, blank=True, null=True)
    u_admin = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_table'
