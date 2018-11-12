
CREATE DATABASE /*!32312 IF NOT EXISTS*/`polls` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `polls`;

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add choice',7,'add_choice'),(20,'Can change choice',7,'change_choice'),(21,'Can delete choice',7,'delete_choice'),(22,'Can add question',8,'add_question'),(23,'Can change question',8,'change_question'),(24,'Can delete question',8,'delete_question'),(25,'Can add picture',9,'add_picture'),(26,'Can change picture',9,'change_picture'),(27,'Can delete picture',9,'delete_picture'),(28,'Can add zixun',10,'add_zixun'),(29,'Can change zixun',10,'change_zixun'),(30,'Can delete zixun',10,'delete_zixun'),(31,'Can add snippet',11,'add_snippet'),(32,'Can change snippet',11,'change_snippet'),(33,'Can delete snippet',11,'delete_snippet'),(34,'Can add ss',12,'add_ss'),(35,'Can change ss',12,'change_ss'),(36,'Can delete ss',12,'delete_ss');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `auth_user` */

insert  into `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) values (1,'pbkdf2_sha256$36000$3KWD7hqscARr$armxyxMCyosXGjdxfJrojSCbofPs8urbvcWft8xzhFY=','2018-11-09 01:50:26.019000',1,'honthion','','','honthion@gmail.com',1,1,'2017-06-19 07:34:22.072060');

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'polls','choice'),(8,'polls','question'),(6,'sessions','session'),(9,'snippets','picture'),(11,'snippets','snippet'),(12,'snippets','ss'),(10,'snippets','zixun');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values (1,'contenttypes','0001_initial','2017-06-16 04:13:27.651253'),(2,'auth','0001_initial','2017-06-16 04:13:41.713188'),(3,'admin','0001_initial','2017-06-16 04:13:44.963247'),(4,'admin','0002_logentry_remove_auto_add','2017-06-16 04:13:47.599392'),(5,'contenttypes','0002_remove_content_type_name','2017-06-16 04:13:49.655879'),(6,'auth','0002_alter_permission_name_max_length','2017-06-16 04:13:50.884250'),(7,'auth','0003_alter_user_email_max_length','2017-06-16 04:13:52.539022'),(8,'auth','0004_alter_user_username_opts','2017-06-16 04:13:55.596097'),(9,'auth','0005_alter_user_last_login_null','2017-06-16 04:13:57.208660'),(10,'auth','0006_require_contenttypes_0002','2017-06-16 04:13:58.184922'),(11,'auth','0007_alter_validators_add_error_messages','2017-06-16 04:13:59.174097'),(12,'auth','0008_alter_user_username_max_length','2017-06-16 04:14:00.404352'),(13,'polls','0001_initial','2017-06-16 04:14:04.176210'),(14,'sessions','0001_initial','2017-06-16 04:14:06.179203'),(15,'snippets','0001_initial','2017-06-19 07:35:59.523283'),(16,'snippets','0002_zixun','2017-06-19 07:36:03.992347'),(17,'snippets','0003_zixun_publish_status','2017-06-19 07:36:07.039829'),(18,'snippets','0004_picture','2017-06-19 07:36:15.876862'),(19,'snippets','0005_ss','2017-06-28 07:42:53.371599');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values ('1jzk1gern9mf6cg48ay5o9kipfjax018','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-03 18:16:56.449610'),('6o4fqhasmju5ylcbwl8fhnw99iqyankq','YWRjNDFkMzFiNzUwMWY4OTIwYzViOWYzMDgyOTJiZjM3MDk0NTJmNzp7Il9hdXRoX3VzZXJfaGFzaCI6ImMwZmU2YmVhOGYyMjRkMzcwYmYzMmUzMTFiMGRhYWMwZDA0OWUxNGQiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-11-23 01:50:26.109000'),('8mijeuleqfucd2xst1ur2o96xoo1pnz4','YzgxMjY3MDkxNjMwNjJmZWNmYTg0ZTAwNWI0ZGYzZjIzMmNkZWJlZjp7fQ==','2018-11-23 01:44:29.640000'),('jdmzg0r6cdanqo4l0pts4tl3kyzhv0k8','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-27 06:28:48.261500'),('jg9balhyj02fuy0s542mqtmgiot8k8o6','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-22 05:59:37.431350'),('kdmf6v2t3d96jrs4u2wjkqd1zn91breu','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-12 07:45:02.407541'),('knwippbssftqlbylf6iia2121lec3378','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-13 02:26:00.149610'),('pwz3wed9l0maf3z3ngjyboaxahnv3unw','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-12 08:18:17.800032'),('tgjhqn2pmc0e19aeods1avfjh6xnisum','MmFiNGM4YWIxOGQwNjNhYjljMmRhYTg1NzgxNDQ3NTc0Y2JmZjAyNzp7Il9hdXRoX3VzZXJfaGFzaCI6IjY4YmFjOTA1Yzg1MzA3ZWViMTNiNGQ1YTE1ODE0ODk5ODllOGM1MzciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2017-07-12 07:11:59.749030'),('xs4uth6438ga5nuebijz4vnonlx7w4hy','YzgxMjY3MDkxNjMwNjJmZWNmYTg0ZTAwNWI0ZGYzZjIzMmNkZWJlZjp7fQ==','2018-11-23 01:44:44.828000');

/*Table structure for table `polls_choice` */

DROP TABLE IF EXISTS `polls_choice`;

CREATE TABLE `polls_choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `choice_text` varchar(200) NOT NULL,
  `votes` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `polls_choice_question_id_c5b4b260_fk_polls_question_id` (`question_id`),
  CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id` FOREIGN KEY (`question_id`) REFERENCES `polls_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `polls_choice` */

/*Table structure for table `polls_question` */

DROP TABLE IF EXISTS `polls_question`;

CREATE TABLE `polls_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` varchar(200) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `polls_question` */

/*Table structure for table `snippets_picture` */

DROP TABLE IF EXISTS `snippets_picture`;

CREATE TABLE `snippets_picture` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `category` longtext NOT NULL,
  `isComment` tinyint(1) NOT NULL,
  `publish_time` longtext NOT NULL,
  `content` longtext NOT NULL,
  `picture_list` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `snippets_picture` */

/*Table structure for table `snippets_snippet` */

DROP TABLE IF EXISTS `snippets_snippet`;

CREATE TABLE `snippets_snippet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `code` longtext NOT NULL,
  `linenos` tinyint(1) NOT NULL,
  `language` varchar(100) NOT NULL,
  `style` varchar(100) NOT NULL,
  `highlighted` longtext NOT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `snippets_snippet_owner_id_20604299_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `snippets_snippet_owner_id_20604299_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `snippets_snippet` */

/*Table structure for table `snippets_ss` */

DROP TABLE IF EXISTS `snippets_ss`;

CREATE TABLE `snippets_ss` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  `qq` longtext NOT NULL,
  `wechat` longtext NOT NULL,
  `alipay` longtext NOT NULL,
  `buy_time` longtext NOT NULL,
  `end_time` longtext NOT NULL,
  `ss_ip` longtext NOT NULL,
  `ss_port` longtext NOT NULL,
  `ss_passwd` longtext NOT NULL,
  `ss_encry` longtext NOT NULL,
  `isExpired` tinyint(1) NOT NULL,
  `note` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Data for the table `snippets_ss` */

insert  into `snippets_ss`(`id`,`created`,`name`,`qq`,`wechat`,`alipay`,`buy_time`,`end_time`,`ss_ip`,`ss_port`,`ss_passwd`,`ss_encry`,`isExpired`,`note`) values (1,'2017-06-28 07:57:02.211866','wangbi','476301176','','','2017-03-20-21-30','2018-03-20-21-30','23.105.219.180','8387','476301176hh2','aes-256-cfb',0,''),(4,'2017-06-28 08:16:57.070830','王豆豆','107900595','','','2017-03-16 16:16:26','2018-03-16 16:16:32','23.105.219.180','8386','107900595dkd8','aes-256-cfb',0,''),(5,'2017-06-28 08:18:09.102603','体验demo','','','','2017-06-28 16:17:52','2018-06-28 16:17:56','23.105.219.180','8380','test4433056ils','aes-256-cfb',0,''),(6,'2017-06-28 08:28:58.477464','自己用','','','','2017-06-28 16:27:35','2017-06-28 16:27:47','23.105.219.180','443','OWQwMGNhMj','aes-256-cfb',0,''),(7,'2017-06-28 08:41:17.010090','百伦demo','','','','2017-06-28 16:40:14','2017-06-28 16:40:19','23.106.157.194','8888','a123456','rc4-md5',0,''),(8,'2017-06-28 08:48:39.660030','linkcool','','','','2017-06-28 16:46:04','','174.139.217.166','34567','localnwk','aes-128-cfb',1,''),(9,'2017-06-29 01:10:22.230970','lindaosong','8482631861','wxid_wc9vjux7r34h22','','2016-12-07 09:09:11','2017-12-07 09:09:48','23.105.219.180','8385','848263186uu2','aes-256-cfb',0,'');

/*Table structure for table `snippets_zixun` */

DROP TABLE IF EXISTS `snippets_zixun`;

CREATE TABLE `snippets_zixun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `category` longtext NOT NULL,
  `source` longtext NOT NULL,
  `update_time` longtext NOT NULL,
  `see_times` longtext NOT NULL,
  `publish_status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `snippets_zixun` */

insert  into `snippets_zixun`(`id`,`created`,`title`,`category`,`source`,`update_time`,`see_times`,`publish_status`) values (1,'2017-06-28 07:52:07.433512','','0','0','','0',1),(2,'2017-06-28 07:52:10.261419','sdfwef','0','0','2017-06-07 15:52:01','0',1);

