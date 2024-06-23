/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024/3/11 12:17:14                           */
/*==============================================================*/


drop table if exists comment_table;

drop table if exists post_table;

drop table if exists post_table_all;

drop table if exists topic_table;

drop table if exists topic_table_all;

/*==============================================================*/
/* Table: comment_table                                         */
/*==============================================================*/
create table comment_table
(
   c_index              bigint not null auto_increment,
   c_audience_id        int,
   c_like_counts        int,
   c_screen_name        varchar(256),
   c_location           varchar(256),
   c_gender             int,
   c_followers_count    int,
   c_friends_count      int,
   c_statuses_count     int,
   c_text_raw           varchar(2048),
   c_mid                bigint,
   primary key (c_index)
);

/*==============================================================*/
/* Table: post_table                                            */
/*==============================================================*/
create table post_table
(
   p_mid                bigint not null,
   p_auther             varchar(256),
   p_txt                varchar(2048),
   p_transmit           int,
   p_comment            int,
   p_like               int,
   t_title              varchar(256),
   p_uid                int,
   p_birthday           varchar(256),
   p_constellation      varchar(256),
   p_created_at         varchar(256),
   p_gender             int,
   p_location           varchar(256),
   p_audence_id         varchar(1024),
   primary key (p_mid)
);

/*==============================================================*/
/* Table: post_table_all                                        */
/*==============================================================*/
create table post_table_all
(
   p_mid                bigint not null,
   p_auther             varchar(256),
   p_txt                varchar(2048),
   p_transmit           int,
   p_comment            int,
   p_like               int,
   p_title              varchar(256),
   p_uid                int,
   primary key (p_mid)
);

/*==============================================================*/
/* Table: topic_table                                           */
/*==============================================================*/
create table topic_table
(
   t_title              varchar(256) not null,
   t_label              varchar(256),
   t_time               varchar(256),
   t_host               varchar(256),
   t_continue           int,
   t_sort               int,
   t_hot                int,
   primary key (t_title)
);

/*==============================================================*/
/* Table: topic_table_all                                       */
/*==============================================================*/
create table topic_table_all
(
   t_index              int not null auto_increment,
   t_title              varchar(256),
   t_label              varchar(256),
   t_time               varchar(256),
   t_host               varchar(256),
   t_continue           int,
   t_sort               int,
   t_hot                int,
   primary key (t_index)
);

alter table comment_table add constraint FK_commend_post_mid_key foreign key (c_mid)
      references post_table (p_mid) on delete restrict on update restrict;

alter table post_table add constraint FK_post_all_key foreign key (p_mid)
      references post_table_all (p_mid) on delete restrict on update restrict;

alter table post_table add constraint FK_post_topic_key foreign key (t_title)
      references topic_table (t_title) on delete restrict on update restrict;

