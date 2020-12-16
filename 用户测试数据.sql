/*
Navicat SQLite Data Transfer

Source Server         : 智服喵Sqlite
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2020-12-14 19:31:12
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for Ask_ask
-- ----------------------------
DROP TABLE IF EXISTS "main"."Ask_ask";
CREATE TABLE "Ask_ask" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "contact_info" varchar(20) NOT NULL, "ask_type" varchar(20) NOT NULL, "reason" varchar(50) NOT NULL, "place" varchar(50) NOT NULL, "ask_state" varchar(5) NOT NULL, "start_time" datetime NOT NULL, "end_time" datetime NOT NULL, "created_time" datetime NOT NULL, "modify_time" datetime NOT NULL, "user_id_id" integer NOT NULL REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED, "grade_id_id" integer NULL REFERENCES "User_grade" ("id") DEFERRABLE INITIALLY DEFERRED, "pass_id_id" integer NOT NULL REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED, "status" varchar(4) NOT NULL);

-- ----------------------------
-- Records of Ask_ask
-- ----------------------------
INSERT INTO "main"."Ask_ask" VALUES (1, 1, 0, 1, 1, 0, '2020-11-14 02:00:00', '2020-11-14 00:00:00', '2020-12-14 17:37:29.676389', '2020-12-14 18:58:15.357823', 13, 1, 9, 3);
INSERT INTO "main"."Ask_ask" VALUES (2, 2, 1, 2, 2, 0, '2020-11-16 02:00:00', '2020-11-14 00:00:00', '2020-12-14 17:37:48.080531', '2020-12-14 18:58:15.973644', 13, 1, 9, 4);
INSERT INTO "main"."Ask_ask" VALUES (3, 1, 2, 3, 3, 0, '2020-12-16 02:00:00', '2020-09-14 00:00:00', '2020-12-14 17:38:06.442127', '2020-12-14 18:48:16.794281', 13, 1, 1, 4);

-- ----------------------------
-- Table structure for Ask_audit
-- ----------------------------
DROP TABLE IF EXISTS "main"."Ask_audit";
CREATE TABLE "Ask_audit" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "explain" varchar(20) NOT NULL, "created_time" datetime NOT NULL, "modify_time" datetime NOT NULL, "ask_id_id" integer NULL REFERENCES "Ask_ask" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED, "status" varchar(4) NOT NULL);

-- ----------------------------
-- Records of Ask_audit
-- ----------------------------
INSERT INTO "main"."Ask_audit" VALUES (1, '', '2020-12-14 18:48:15.313932', '2020-12-14 18:48:15.313932', 1, 1, 3);
INSERT INTO "main"."Ask_audit" VALUES (2, '', '2020-12-14 18:48:15.991985', '2020-12-14 18:48:15.991985', 2, 1, 2);
INSERT INTO "main"."Ask_audit" VALUES (3, '', '2020-12-14 18:48:16.802533', '2020-12-14 18:48:16.802533', 3, 1, 4);
INSERT INTO "main"."Ask_audit" VALUES (4, '', '2020-12-14 18:56:56.595671', '2020-12-14 18:56:56.595671', 2, 9, 3);
INSERT INTO "main"."Ask_audit" VALUES (5, '', '2020-12-14 18:58:15.369617', '2020-12-14 18:58:15.369617', 1, 9, 3);
INSERT INTO "main"."Ask_audit" VALUES (6, '', '2020-12-14 18:58:15.984742', '2020-12-14 18:58:15.984742', 2, 9, 4);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_group";
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_group_permissions";
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_permission";
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO "main"."auth_permission" VALUES (1, 1, 'add_logentry', 'Can add log entry');
INSERT INTO "main"."auth_permission" VALUES (2, 1, 'change_logentry', 'Can change log entry');
INSERT INTO "main"."auth_permission" VALUES (3, 1, 'delete_logentry', 'Can delete log entry');
INSERT INTO "main"."auth_permission" VALUES (4, 1, 'view_logentry', 'Can view log entry');
INSERT INTO "main"."auth_permission" VALUES (5, 2, 'add_permission', 'Can add permission');
INSERT INTO "main"."auth_permission" VALUES (6, 2, 'change_permission', 'Can change permission');
INSERT INTO "main"."auth_permission" VALUES (7, 2, 'delete_permission', 'Can delete permission');
INSERT INTO "main"."auth_permission" VALUES (8, 2, 'view_permission', 'Can view permission');
INSERT INTO "main"."auth_permission" VALUES (9, 3, 'add_group', 'Can add group');
INSERT INTO "main"."auth_permission" VALUES (10, 3, 'change_group', 'Can change group');
INSERT INTO "main"."auth_permission" VALUES (11, 3, 'delete_group', 'Can delete group');
INSERT INTO "main"."auth_permission" VALUES (12, 3, 'view_group', 'Can view group');
INSERT INTO "main"."auth_permission" VALUES (13, 4, 'add_user', 'Can add user');
INSERT INTO "main"."auth_permission" VALUES (14, 4, 'change_user', 'Can change user');
INSERT INTO "main"."auth_permission" VALUES (15, 4, 'delete_user', 'Can delete user');
INSERT INTO "main"."auth_permission" VALUES (16, 4, 'view_user', 'Can view user');
INSERT INTO "main"."auth_permission" VALUES (17, 5, 'add_contenttype', 'Can add content type');
INSERT INTO "main"."auth_permission" VALUES (18, 5, 'change_contenttype', 'Can change content type');
INSERT INTO "main"."auth_permission" VALUES (19, 5, 'delete_contenttype', 'Can delete content type');
INSERT INTO "main"."auth_permission" VALUES (20, 5, 'view_contenttype', 'Can view content type');
INSERT INTO "main"."auth_permission" VALUES (21, 6, 'add_session', 'Can add session');
INSERT INTO "main"."auth_permission" VALUES (22, 6, 'change_session', 'Can change session');
INSERT INTO "main"."auth_permission" VALUES (23, 6, 'delete_session', 'Can delete session');
INSERT INTO "main"."auth_permission" VALUES (24, 6, 'view_session', 'Can view session');
INSERT INTO "main"."auth_permission" VALUES (25, 7, 'add_ask', 'Can add 请假条');
INSERT INTO "main"."auth_permission" VALUES (26, 7, 'change_ask', 'Can change 请假条');
INSERT INTO "main"."auth_permission" VALUES (27, 7, 'delete_ask', 'Can delete 请假条');
INSERT INTO "main"."auth_permission" VALUES (28, 7, 'view_ask', 'Can view 请假条');
INSERT INTO "main"."auth_permission" VALUES (29, 8, 'add_audit', 'Can add 审核情况表');
INSERT INTO "main"."auth_permission" VALUES (30, 8, 'change_audit', 'Can change 审核情况表');
INSERT INTO "main"."auth_permission" VALUES (31, 8, 'delete_audit', 'Can delete 审核情况表');
INSERT INTO "main"."auth_permission" VALUES (32, 8, 'view_audit', 'Can view 审核情况表');
INSERT INTO "main"."auth_permission" VALUES (33, 9, 'add_college', 'Can add 分院');
INSERT INTO "main"."auth_permission" VALUES (34, 9, 'change_college', 'Can change 分院');
INSERT INTO "main"."auth_permission" VALUES (35, 9, 'delete_college', 'Can delete 分院');
INSERT INTO "main"."auth_permission" VALUES (36, 9, 'view_college', 'Can view 分院');
INSERT INTO "main"."auth_permission" VALUES (37, 10, 'add_grade', 'Can add 班级');
INSERT INTO "main"."auth_permission" VALUES (38, 10, 'change_grade', 'Can change 班级');
INSERT INTO "main"."auth_permission" VALUES (39, 10, 'delete_grade', 'Can delete 班级');
INSERT INTO "main"."auth_permission" VALUES (40, 10, 'view_grade', 'Can view 班级');
INSERT INTO "main"."auth_permission" VALUES (41, 11, 'add_permission', 'Can add 权限');
INSERT INTO "main"."auth_permission" VALUES (42, 11, 'change_permission', 'Can change 权限');
INSERT INTO "main"."auth_permission" VALUES (43, 11, 'delete_permission', 'Can delete 权限');
INSERT INTO "main"."auth_permission" VALUES (44, 11, 'view_permission', 'Can view 权限');
INSERT INTO "main"."auth_permission" VALUES (45, 12, 'add_user', 'Can add 用户');
INSERT INTO "main"."auth_permission" VALUES (46, 12, 'change_user', 'Can change 用户');
INSERT INTO "main"."auth_permission" VALUES (47, 12, 'delete_user', 'Can delete 用户');
INSERT INTO "main"."auth_permission" VALUES (48, 12, 'view_user', 'Can view 用户');
INSERT INTO "main"."auth_permission" VALUES (49, 13, 'add_userinfo', 'Can add 用户信息');
INSERT INTO "main"."auth_permission" VALUES (50, 13, 'change_userinfo', 'Can change 用户信息');
INSERT INTO "main"."auth_permission" VALUES (51, 13, 'delete_userinfo', 'Can delete 用户信息');
INSERT INTO "main"."auth_permission" VALUES (52, 13, 'view_userinfo', 'Can view 用户信息');
INSERT INTO "main"."auth_permission" VALUES (53, 14, 'add_userforpermission', 'Can add 用户权限表');
INSERT INTO "main"."auth_permission" VALUES (54, 14, 'change_userforpermission', 'Can change 用户权限表');
INSERT INTO "main"."auth_permission" VALUES (55, 14, 'delete_userforpermission', 'Can delete 用户权限表');
INSERT INTO "main"."auth_permission" VALUES (56, 14, 'view_userforpermission', 'Can view 用户权限表');
INSERT INTO "main"."auth_permission" VALUES (57, 15, 'add_token', 'Can add 用户token');
INSERT INTO "main"."auth_permission" VALUES (58, 15, 'change_token', 'Can change 用户token');
INSERT INTO "main"."auth_permission" VALUES (59, 15, 'delete_token', 'Can delete 用户token');
INSERT INTO "main"."auth_permission" VALUES (60, 15, 'view_token', 'Can view 用户token');
INSERT INTO "main"."auth_permission" VALUES (61, 16, 'add_teacherinfo', 'Can add 老师信息');
INSERT INTO "main"."auth_permission" VALUES (62, 16, 'change_teacherinfo', 'Can change 老师信息');
INSERT INTO "main"."auth_permission" VALUES (63, 16, 'delete_teacherinfo', 'Can delete 老师信息');
INSERT INTO "main"."auth_permission" VALUES (64, 16, 'view_teacherinfo', 'Can view 老师信息');
INSERT INTO "main"."auth_permission" VALUES (65, 17, 'add_teacherforgrade', 'Can add 教师班级关系');
INSERT INTO "main"."auth_permission" VALUES (66, 17, 'change_teacherforgrade', 'Can change 教师班级关系');
INSERT INTO "main"."auth_permission" VALUES (67, 17, 'delete_teacherforgrade', 'Can delete 教师班级关系');
INSERT INTO "main"."auth_permission" VALUES (68, 17, 'view_teacherforgrade', 'Can view 教师班级关系');
INSERT INTO "main"."auth_permission" VALUES (69, 18, 'add_teacherforcollege', 'Can add 教师院级关系');
INSERT INTO "main"."auth_permission" VALUES (70, 18, 'change_teacherforcollege', 'Can change 教师院级关系');
INSERT INTO "main"."auth_permission" VALUES (71, 18, 'delete_teacherforcollege', 'Can delete 教师院级关系');
INSERT INTO "main"."auth_permission" VALUES (72, 18, 'view_teacherforcollege', 'Can view 教师院级关系');
INSERT INTO "main"."auth_permission" VALUES (73, 19, 'add_studentinfo', 'Can add 学生信息');
INSERT INTO "main"."auth_permission" VALUES (74, 19, 'change_studentinfo', 'Can change 学生信息');
INSERT INTO "main"."auth_permission" VALUES (75, 19, 'delete_studentinfo', 'Can delete 学生信息');
INSERT INTO "main"."auth_permission" VALUES (76, 19, 'view_studentinfo', 'Can view 学生信息');
INSERT INTO "main"."auth_permission" VALUES (77, 20, 'add_tpost', 'Can add 第三方账户');
INSERT INTO "main"."auth_permission" VALUES (78, 20, 'change_tpost', 'Can change 第三方账户');
INSERT INTO "main"."auth_permission" VALUES (79, 20, 'delete_tpost', 'Can delete 第三方账户');
INSERT INTO "main"."auth_permission" VALUES (80, 20, 'view_tpost', 'Can view 第三方账户');
INSERT INTO "main"."auth_permission" VALUES (81, 21, 'add_career', 'Can add 就业信息表');
INSERT INTO "main"."auth_permission" VALUES (82, 21, 'change_career', 'Can change 就业信息表');
INSERT INTO "main"."auth_permission" VALUES (83, 21, 'delete_career', 'Can delete 就业信息表');
INSERT INTO "main"."auth_permission" VALUES (84, 21, 'view_career', 'Can view 就业信息表');
INSERT INTO "main"."auth_permission" VALUES (85, 22, 'add_primitives', 'Can add 分类主表');
INSERT INTO "main"."auth_permission" VALUES (86, 22, 'change_primitives', 'Can change 分类主表');
INSERT INTO "main"."auth_permission" VALUES (87, 22, 'delete_primitives', 'Can delete 分类主表');
INSERT INTO "main"."auth_permission" VALUES (88, 22, 'view_primitives', 'Can view 分类主表');
INSERT INTO "main"."auth_permission" VALUES (89, 23, 'add_typepar', 'Can add 分类父表');
INSERT INTO "main"."auth_permission" VALUES (90, 23, 'change_typepar', 'Can change 分类父表');
INSERT INTO "main"."auth_permission" VALUES (91, 23, 'delete_typepar', 'Can delete 分类父表');
INSERT INTO "main"."auth_permission" VALUES (92, 23, 'view_typepar', 'Can view 分类父表');
INSERT INTO "main"."auth_permission" VALUES (93, 24, 'add_typechild', 'Can add 分类子表');
INSERT INTO "main"."auth_permission" VALUES (94, 24, 'change_typechild', 'Can change 分类子表');
INSERT INTO "main"."auth_permission" VALUES (95, 24, 'delete_typechild', 'Can delete 分类子表');
INSERT INTO "main"."auth_permission" VALUES (96, 24, 'view_typechild', 'Can view 分类子表');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_user";
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO "main"."auth_user" VALUES (1, 'pbkdf2_sha256$216000$H2g4GAUfqG7j$2I30mFFVDSKMgKiy+hTDKsEZ6sPPqJEinsWStqXv858=', '2020-12-14 16:07:52.949169', 1, 'qiuzhe', '', '', 1, 1, '2020-12-14 16:07:35.765287', '');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_user_groups";
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "main"."auth_user_user_permissions";
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for Career_career
-- ----------------------------
DROP TABLE IF EXISTS "main"."Career_career";
CREATE TABLE "Career_career" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "note" varchar(300) NOT NULL, "text" varchar(999) NOT NULL, "source" varchar(100) NOT NULL, "viewnum" integer NOT NULL, "release_time" datetime NOT NULL);

-- ----------------------------
-- Records of Career_career
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_admin_log";
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0));

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO "main"."django_admin_log" VALUES (1, '2020-12-14 16:08:21.803936', 1, 'admin1', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (2, '2020-12-14 16:08:27.404465', 2, 'admin2', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (3, '2020-12-14 16:08:31.817751', 3, 'admin3', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (4, '2020-12-14 16:08:36.787505', 4, 'admin4', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (5, '2020-12-14 16:08:41.178075', 5, 'admin5', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (6, '2020-12-14 16:08:48.099227', 6, 'admin6', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (7, '2020-12-14 16:08:53.235120', 7, 'admin7', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (8, '2020-12-14 16:08:58.796870', 8, 'admin8', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (9, '2020-12-14 16:09:04.811529', 9, 'admin9', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (10, '2020-12-14 16:09:11.442273', 10, 'admin10', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (11, '2020-12-14 16:09:23.123222', 11, 'admin11', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (12, '2020-12-14 16:09:28.587462', 12, 'admin12', '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (13, '2020-12-14 16:10:20.931279', 13, 19510146, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (14, '2020-12-14 16:10:25.729893', 14, 19510129, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (15, '2020-12-14 16:10:33.251349', 15, 19510201, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (16, '2020-12-14 16:10:37.705410', 16, 19510202, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (17, '2020-12-14 16:10:55.931673', 17, 20210101, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (18, '2020-12-14 16:11:01.323033', 18, 20210102, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (19, '2020-12-14 16:11:11.739253', 19, 20210201, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (20, '2020-12-14 16:11:15.761120', 20, 20210202, '[{"added": {}}]', 12, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (21, '2020-12-14 16:12:13.430039', 1, '老师9', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (22, '2020-12-14 16:12:28.453918', 2, '老师10', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (23, '2020-12-14 16:12:32.742714', 1, '老师9', '[{"changed": {"fields": ["\u8eab\u4efd"]}}]', 13, 1, 2);
INSERT INTO "main"."django_admin_log" VALUES (24, '2020-12-14 16:12:45.637104', 3, '老师1', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (25, '2020-12-14 16:12:54.686313', 4, '老师2', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (26, '2020-12-14 16:13:03.941369', 5, '老师3', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (27, '2020-12-14 16:13:28.808644', 6, '老师11', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (28, '2020-12-14 16:13:39.998592', 7, '老师5', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (29, '2020-12-14 16:13:49.944260', 8, '老师6', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (30, '2020-12-14 16:14:06.197296', 9, '老师7', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (31, '2020-12-14 16:14:14.101804', 10, '老师8', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (32, '2020-12-14 16:14:46.176595', 11, '邹洋', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (33, '2020-12-14 16:15:01.144857', 12, '罗国军', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (34, '2020-12-14 16:15:46.750185', 13, 19510201, '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (35, '2020-12-14 16:16:03.505411', 13, '张三1', '[{"changed": {"fields": ["\u59d3\u540d", "\u7535\u8bdd"]}}]', 13, 1, 2);
INSERT INTO "main"."django_admin_log" VALUES (36, '2020-12-14 16:16:13.417796', 14, '张三2', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (37, '2020-12-14 16:16:27.108497', 15, '李四1', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (38, '2020-12-14 16:16:33.840085', 16, '李四2', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (39, '2020-12-14 16:16:44.866617', 17, '王五1', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (40, '2020-12-14 16:16:58.233200', 18, '王五2', '[{"added": {}}]', 13, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (41, '2020-12-14 17:22:23.586717', 1, '智慧交通学院', '[{"added": {}}]', 9, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (42, '2020-12-14 17:22:25.419292', 1, 195101, '[{"added": {}}]', 10, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (43, '2020-12-14 17:22:46.659254', 2, '轨道交通学院', '[{"added": {}}]', 9, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (44, '2020-12-14 17:23:01.500053', 2, 202101, '[{"added": {}}]', 10, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (45, '2020-12-14 17:23:13.272517', 3, 202102, '[{"added": {}}]', 10, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (46, '2020-12-14 17:23:28.003260', 4, 195102, '[{"added": {}}]', 10, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (47, '2020-12-14 17:26:06.893967', 1, 'StudentInfo object (1)', '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (48, '2020-12-14 17:26:32.957403', 2, 19510129, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (49, '2020-12-14 17:26:55.546173', 3, 19510201, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (50, '2020-12-14 17:27:06.306567', 4, 19510202, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (51, '2020-12-14 17:27:20.217188', 5, 20210101, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (52, '2020-12-14 17:27:38.121195', 6, 20210102, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (53, '2020-12-14 17:27:45.473477', 7, 20210201, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (54, '2020-12-14 17:27:52.858349', 8, 20210202, '[{"added": {}}]', 19, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (55, '2020-12-14 17:31:57.385447', 1, 'TeacherForGrade object (1)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (56, '2020-12-14 17:32:01.502328', 2, 'TeacherForGrade object (2)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (57, '2020-12-14 17:32:08.185313', 3, 'TeacherForGrade object (3)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (58, '2020-12-14 17:32:14.224810', 4, 'TeacherForGrade object (4)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (59, '2020-12-14 17:32:30.449808', 5, 'TeacherForGrade object (5)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (60, '2020-12-14 17:32:38.480840', 6, 'TeacherForGrade object (6)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (61, '2020-12-14 17:32:50.265465', 7, 'TeacherForGrade object (7)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (62, '2020-12-14 17:32:53.792262', 8, 'TeacherForGrade object (8)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (63, '2020-12-14 17:33:40.986303', 1, 'TeacherForCollege object (1)', '[{"added": {}}]', 18, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (64, '2020-12-14 17:33:44.897768', 2, 'TeacherForCollege object (2)', '[{"added": {}}]', 18, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (65, '2020-12-14 17:33:49.209514', 3, 'TeacherForCollege object (3)', '[{"added": {}}]', 18, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (66, '2020-12-14 17:34:07.745351', 4, 'TeacherForCollege object (4)', '[{"added": {}}]', 18, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (67, '2020-12-14 17:34:18.055866', 9, 'TeacherForGrade object (9)', '[{"added": {}}]', 17, 1, 1);
INSERT INTO "main"."django_admin_log" VALUES (68, '2020-12-14 18:12:40.039862', 19, '老师12', '[{"added": {}}]', 13, 1, 1);

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_content_type";
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO "main"."django_content_type" VALUES (1, 'admin', 'logentry');
INSERT INTO "main"."django_content_type" VALUES (2, 'auth', 'permission');
INSERT INTO "main"."django_content_type" VALUES (3, 'auth', 'group');
INSERT INTO "main"."django_content_type" VALUES (4, 'auth', 'user');
INSERT INTO "main"."django_content_type" VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO "main"."django_content_type" VALUES (6, 'sessions', 'session');
INSERT INTO "main"."django_content_type" VALUES (7, 'Ask', 'ask');
INSERT INTO "main"."django_content_type" VALUES (8, 'Ask', 'audit');
INSERT INTO "main"."django_content_type" VALUES (9, 'User', 'college');
INSERT INTO "main"."django_content_type" VALUES (10, 'User', 'grade');
INSERT INTO "main"."django_content_type" VALUES (11, 'User', 'permission');
INSERT INTO "main"."django_content_type" VALUES (12, 'User', 'user');
INSERT INTO "main"."django_content_type" VALUES (13, 'User', 'userinfo');
INSERT INTO "main"."django_content_type" VALUES (14, 'User', 'userforpermission');
INSERT INTO "main"."django_content_type" VALUES (15, 'User', 'token');
INSERT INTO "main"."django_content_type" VALUES (16, 'User', 'teacherinfo');
INSERT INTO "main"."django_content_type" VALUES (17, 'User', 'teacherforgrade');
INSERT INTO "main"."django_content_type" VALUES (18, 'User', 'teacherforcollege');
INSERT INTO "main"."django_content_type" VALUES (19, 'User', 'studentinfo');
INSERT INTO "main"."django_content_type" VALUES (20, 'User', 'tpost');
INSERT INTO "main"."django_content_type" VALUES (21, 'Career', 'career');
INSERT INTO "main"."django_content_type" VALUES (22, 'Manage', 'primitives');
INSERT INTO "main"."django_content_type" VALUES (23, 'Manage', 'typepar');
INSERT INTO "main"."django_content_type" VALUES (24, 'Manage', 'typechild');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_migrations";
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO "main"."django_migrations" VALUES (1, 'User', '0001_initial', '2020-12-14 16:07:19.389399');
INSERT INTO "main"."django_migrations" VALUES (2, 'Ask', '0001_initial', '2020-12-14 16:07:19.415402');
INSERT INTO "main"."django_migrations" VALUES (3, 'Ask', '0002_ask_grade_id', '2020-12-14 16:07:19.433355');
INSERT INTO "main"."django_migrations" VALUES (4, 'Ask', '0003_ask_pass_id', '2020-12-14 16:07:19.452691');
INSERT INTO "main"."django_migrations" VALUES (5, 'Ask', '0004_auto_20201126_1103', '2020-12-14 16:07:19.470752');
INSERT INTO "main"."django_migrations" VALUES (6, 'Ask', '0005_auto_20201214_1217', '2020-12-14 16:07:19.496715');
INSERT INTO "main"."django_migrations" VALUES (7, 'Ask', '0006_auto_20201214_1607', '2020-12-14 16:07:19.529091');
INSERT INTO "main"."django_migrations" VALUES (8, 'Career', '0001_initial', '2020-12-14 16:07:19.539065');
INSERT INTO "main"."django_migrations" VALUES (9, 'Manage', '0001_initial', '2020-12-14 16:07:19.551032');
INSERT INTO "main"."django_migrations" VALUES (10, 'User', '0002_auto_20201126_1132', '2020-12-14 16:07:19.570234');
INSERT INTO "main"."django_migrations" VALUES (11, 'User', '0003_auto_20201126_1136', '2020-12-14 16:07:19.587189');
INSERT INTO "main"."django_migrations" VALUES (12, 'User', '0004_auto_20201212_2106', '2020-12-14 16:07:19.612126');
INSERT INTO "main"."django_migrations" VALUES (13, 'User', '0005_auto_20201213_0946', '2020-12-14 16:07:19.636138');
INSERT INTO "main"."django_migrations" VALUES (14, 'User', '0006_auto_20201213_0952', '2020-12-14 16:07:19.662154');
INSERT INTO "main"."django_migrations" VALUES (15, 'contenttypes', '0001_initial', '2020-12-14 16:07:19.673098');
INSERT INTO "main"."django_migrations" VALUES (16, 'auth', '0001_initial', '2020-12-14 16:07:19.694682');
INSERT INTO "main"."django_migrations" VALUES (17, 'admin', '0001_initial', '2020-12-14 16:07:19.713672');
INSERT INTO "main"."django_migrations" VALUES (18, 'admin', '0002_logentry_remove_auto_add', '2020-12-14 16:07:19.729002');
INSERT INTO "main"."django_migrations" VALUES (19, 'admin', '0003_logentry_add_action_flag_choices', '2020-12-14 16:07:19.744842');
INSERT INTO "main"."django_migrations" VALUES (20, 'contenttypes', '0002_remove_content_type_name', '2020-12-14 16:07:19.778811');
INSERT INTO "main"."django_migrations" VALUES (21, 'auth', '0002_alter_permission_name_max_length', '2020-12-14 16:07:19.795872');
INSERT INTO "main"."django_migrations" VALUES (22, 'auth', '0003_alter_user_email_max_length', '2020-12-14 16:07:19.811694');
INSERT INTO "main"."django_migrations" VALUES (23, 'auth', '0004_alter_user_username_opts', '2020-12-14 16:07:19.827074');
INSERT INTO "main"."django_migrations" VALUES (24, 'auth', '0005_alter_user_last_login_null', '2020-12-14 16:07:19.845118');
INSERT INTO "main"."django_migrations" VALUES (25, 'auth', '0006_require_contenttypes_0002', '2020-12-14 16:07:19.851102');
INSERT INTO "main"."django_migrations" VALUES (26, 'auth', '0007_alter_validators_add_error_messages', '2020-12-14 16:07:19.867142');
INSERT INTO "main"."django_migrations" VALUES (27, 'auth', '0008_alter_user_username_max_length', '2020-12-14 16:07:19.885123');
INSERT INTO "main"."django_migrations" VALUES (28, 'auth', '0009_alter_user_last_name_max_length', '2020-12-14 16:07:19.901139');
INSERT INTO "main"."django_migrations" VALUES (29, 'auth', '0010_alter_group_name_max_length', '2020-12-14 16:07:19.917068');
INSERT INTO "main"."django_migrations" VALUES (30, 'auth', '0011_update_proxy_permissions', '2020-12-14 16:07:19.940035');
INSERT INTO "main"."django_migrations" VALUES (31, 'auth', '0012_alter_user_first_name_max_length', '2020-12-14 16:07:19.956990');
INSERT INTO "main"."django_migrations" VALUES (32, 'sessions', '0001_initial', '2020-12-14 16:07:19.982971');
INSERT INTO "main"."django_migrations" VALUES (33, 'User', '0007_remove_studentinfo_student_id', '2020-12-14 17:20:36.554692');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "main"."django_session";
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO "main"."django_session" VALUES ('ilx1aoybf8uvsxgvg8xo9vfaqq9shsef', '.eJxVjEEOwiAQRe_C2hBgOlhcuu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERWpx-t0DxkeoO-E711mRsdV3mIHdFHrTLqXF6Xg_376BQL9_aGBWDHRlMVA7YQQwwnLPGBDgQO0VZgRsNcMoWkQdUjjOjzVkHY7V4fwDT9zeg:1koitc:d0yqxAmz_JULNfYUccG2Yi3hxvZsUZMD8QxugJ3iWNM', '2020-12-28 16:07:52.958148');

-- ----------------------------
-- Table structure for Manage_primitives
-- ----------------------------
DROP TABLE IF EXISTS "main"."Manage_primitives";
CREATE TABLE "Manage_primitives" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(30) NOT NULL);

-- ----------------------------
-- Records of Manage_primitives
-- ----------------------------

-- ----------------------------
-- Table structure for Manage_typechild
-- ----------------------------
DROP TABLE IF EXISTS "main"."Manage_typechild";
CREATE TABLE "Manage_typechild" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(30) NOT NULL, "par_id_id" integer NOT NULL REFERENCES "Manage_typechild" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of Manage_typechild
-- ----------------------------

-- ----------------------------
-- Table structure for Manage_typepar
-- ----------------------------
DROP TABLE IF EXISTS "main"."Manage_typepar";
CREATE TABLE "Manage_typepar" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(30) NOT NULL, "par_id_id" integer NOT NULL REFERENCES "Manage_primitives" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of Manage_typepar
-- ----------------------------

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "main"."sqlite_sequence";
CREATE TABLE sqlite_sequence(name,seq);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
INSERT INTO "main"."sqlite_sequence" VALUES ('django_migrations', 33);
INSERT INTO "main"."sqlite_sequence" VALUES ('Ask_ask', 3);
INSERT INTO "main"."sqlite_sequence" VALUES ('Ask_audit', 6);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_userinfo', 19);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_token', 7);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_tpost', 1);
INSERT INTO "main"."sqlite_sequence" VALUES ('django_admin_log', 68);
INSERT INTO "main"."sqlite_sequence" VALUES ('django_content_type', 24);
INSERT INTO "main"."sqlite_sequence" VALUES ('auth_permission', 96);
INSERT INTO "main"."sqlite_sequence" VALUES ('auth_group', 0);
INSERT INTO "main"."sqlite_sequence" VALUES ('auth_user', 1);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_user', 20);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_studentinfo', 8);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_college', 2);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_grade', 4);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_teacherforgrade', 9);
INSERT INTO "main"."sqlite_sequence" VALUES ('User_teacherforcollege', 4);

-- ----------------------------
-- Table structure for User_college
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_college";
CREATE TABLE "User_college" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);

-- ----------------------------
-- Records of User_college
-- ----------------------------
INSERT INTO "main"."User_college" VALUES (1, '智慧交通学院');
INSERT INTO "main"."User_college" VALUES (2, '轨道交通学院');

-- ----------------------------
-- Table structure for User_grade
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_grade";
CREATE TABLE "User_grade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "college_id_id" integer NOT NULL REFERENCES "User_college" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_grade
-- ----------------------------
INSERT INTO "main"."User_grade" VALUES (1, 195101, 1);
INSERT INTO "main"."User_grade" VALUES (2, 202101, 2);
INSERT INTO "main"."User_grade" VALUES (3, 202102, 2);
INSERT INTO "main"."User_grade" VALUES (4, 195102, 1);

-- ----------------------------
-- Table structure for User_permission
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_permission";
CREATE TABLE "User_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "message" varchar(50) NOT NULL);

-- ----------------------------
-- Records of User_permission
-- ----------------------------

-- ----------------------------
-- Table structure for User_studentinfo
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_studentinfo";
CREATE TABLE "User_studentinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "grade_id_id" integer NOT NULL REFERENCES "User_grade" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL UNIQUE REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_studentinfo
-- ----------------------------
INSERT INTO "main"."User_studentinfo" VALUES (1, 1, 13);
INSERT INTO "main"."User_studentinfo" VALUES (2, 1, 14);
INSERT INTO "main"."User_studentinfo" VALUES (3, 4, 15);
INSERT INTO "main"."User_studentinfo" VALUES (4, 4, 16);
INSERT INTO "main"."User_studentinfo" VALUES (5, 2, 17);
INSERT INTO "main"."User_studentinfo" VALUES (6, 2, 18);
INSERT INTO "main"."User_studentinfo" VALUES (7, 3, 19);
INSERT INTO "main"."User_studentinfo" VALUES (8, 3, 20);

-- ----------------------------
-- Table structure for User_teacherforcollege
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_teacherforcollege";
CREATE TABLE "User_teacherforcollege" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "college_id_id" integer NOT NULL REFERENCES "User_college" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_teacherforcollege
-- ----------------------------
INSERT INTO "main"."User_teacherforcollege" VALUES (1, 1, 9);
INSERT INTO "main"."User_teacherforcollege" VALUES (2, 1, 10);
INSERT INTO "main"."User_teacherforcollege" VALUES (3, 2, 11);
INSERT INTO "main"."User_teacherforcollege" VALUES (4, 1, 12);

-- ----------------------------
-- Table structure for User_teacherforgrade
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_teacherforgrade";
CREATE TABLE "User_teacherforgrade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "grade_id_id" integer NOT NULL REFERENCES "User_grade" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_teacherforgrade
-- ----------------------------
INSERT INTO "main"."User_teacherforgrade" VALUES (1, 1, 1);
INSERT INTO "main"."User_teacherforgrade" VALUES (2, 1, 2);
INSERT INTO "main"."User_teacherforgrade" VALUES (3, 4, 3);
INSERT INTO "main"."User_teacherforgrade" VALUES (4, 4, 4);
INSERT INTO "main"."User_teacherforgrade" VALUES (5, 2, 5);
INSERT INTO "main"."User_teacherforgrade" VALUES (6, 2, 6);
INSERT INTO "main"."User_teacherforgrade" VALUES (7, 3, 7);
INSERT INTO "main"."User_teacherforgrade" VALUES (8, 3, 8);
INSERT INTO "main"."User_teacherforgrade" VALUES (9, 1, 12);

-- ----------------------------
-- Table structure for User_teacherinfo
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_teacherinfo";
CREATE TABLE "User_teacherinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "teacher_extra_info" varchar(50) NOT NULL, "user_id_id" integer NOT NULL UNIQUE REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_teacherinfo
-- ----------------------------

-- ----------------------------
-- Table structure for User_token
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_token";
CREATE TABLE "User_token" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" varchar(100) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_token
-- ----------------------------
INSERT INTO "main"."User_token" VALUES (1, '480403dc5aedbdaf25a3024c6080c95d', 1);
INSERT INTO "main"."User_token" VALUES (2, '3eecfc22841b04fb4303f218baf23f4d', 13);
INSERT INTO "main"."User_token" VALUES (3, '87b3f21fe544046c292a67ff598f9dd8', 2);
INSERT INTO "main"."User_token" VALUES (4, 'c50abb7bd989357f7d2a08bf1e2936db', 9);
INSERT INTO "main"."User_token" VALUES (5, '6ca84f686d9604670b47cb2be82deb1b', 12);
INSERT INTO "main"."User_token" VALUES (6, 'e89fd677b1ba496c1397c9aaaaf99599', 10);
INSERT INTO "main"."User_token" VALUES (7, 'fb7c10908920b8fa157c756c7ffe0d96', 3);

-- ----------------------------
-- Table structure for User_tpost
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_tpost";
CREATE TABLE "User_tpost" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL UNIQUE REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED, "wx_openid" varchar(128) NULL);

-- ----------------------------
-- Records of User_tpost
-- ----------------------------
INSERT INTO "main"."User_tpost" VALUES (1, 13, 'orL5J48DSmP_2D65XVvB3S9khWII');

-- ----------------------------
-- Table structure for User_user
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_user";
CREATE TABLE "User_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_name" varchar(20) NOT NULL, "pass_word" varchar(20) NOT NULL);

-- ----------------------------
-- Records of User_user
-- ----------------------------
INSERT INTO "main"."User_user" VALUES (1, 'admin1', 123456);
INSERT INTO "main"."User_user" VALUES (2, 'admin2', 123456);
INSERT INTO "main"."User_user" VALUES (3, 'admin3', 123456);
INSERT INTO "main"."User_user" VALUES (4, 'admin4', 123456);
INSERT INTO "main"."User_user" VALUES (5, 'admin5', 123456);
INSERT INTO "main"."User_user" VALUES (6, 'admin6', 123456);
INSERT INTO "main"."User_user" VALUES (7, 'admin7', 123456);
INSERT INTO "main"."User_user" VALUES (8, 'admin8', 123456);
INSERT INTO "main"."User_user" VALUES (9, 'admin9', 123456);
INSERT INTO "main"."User_user" VALUES (10, 'admin10', 123456);
INSERT INTO "main"."User_user" VALUES (11, 'admin11', 123456);
INSERT INTO "main"."User_user" VALUES (12, 'admin12', 123456);
INSERT INTO "main"."User_user" VALUES (13, 19510146, 123456);
INSERT INTO "main"."User_user" VALUES (14, 19510129, 123456);
INSERT INTO "main"."User_user" VALUES (15, 19510201, 123456);
INSERT INTO "main"."User_user" VALUES (16, 19510202, 123456);
INSERT INTO "main"."User_user" VALUES (17, 20210101, 123456);
INSERT INTO "main"."User_user" VALUES (18, 20210102, 123456);
INSERT INTO "main"."User_user" VALUES (19, 20210201, 123456);
INSERT INTO "main"."User_user" VALUES (20, 20210202, 123456);

-- ----------------------------
-- Table structure for User_userforpermission
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_userforpermission";
CREATE TABLE "User_userforpermission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "perm_id_id" integer NOT NULL REFERENCES "User_permission" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id_id" integer NOT NULL REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_userforpermission
-- ----------------------------

-- ----------------------------
-- Table structure for User_userinfo
-- ----------------------------
DROP TABLE IF EXISTS "main"."User_userinfo";
CREATE TABLE "User_userinfo" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(20) NOT NULL, "tel" varchar(20) NOT NULL, "identity" varchar(20) NOT NULL, "user_id_id" integer NOT NULL UNIQUE REFERENCES "User_user" ("id") DEFERRABLE INITIALLY DEFERRED);

-- ----------------------------
-- Records of User_userinfo
-- ----------------------------
INSERT INTO "main"."User_userinfo" VALUES (1, '老师9', 9, 'college', 9);
INSERT INTO "main"."User_userinfo" VALUES (2, '老师10', 10, 'college', 10);
INSERT INTO "main"."User_userinfo" VALUES (3, '老师1', 1, 'teacher', 1);
INSERT INTO "main"."User_userinfo" VALUES (4, '老师2', 2, 'teacher', 2);
INSERT INTO "main"."User_userinfo" VALUES (5, '老师3', 3, 'teacher', 3);
INSERT INTO "main"."User_userinfo" VALUES (6, '老师11', 11, 'student', 11);
INSERT INTO "main"."User_userinfo" VALUES (7, '老师5', 5, 'teacher', 5);
INSERT INTO "main"."User_userinfo" VALUES (8, '老师6', 6, 'teacher', 6);
INSERT INTO "main"."User_userinfo" VALUES (9, '老师7', 7, 'teacher', 7);
INSERT INTO "main"."User_userinfo" VALUES (10, '老师8', 8, 'teacher', 8);
INSERT INTO "main"."User_userinfo" VALUES (11, '邹洋', 18329126326, 'student', 13);
INSERT INTO "main"."User_userinfo" VALUES (12, '罗国军', 18329126326, 'student', 14);
INSERT INTO "main"."User_userinfo" VALUES (13, '张三1', 18329126326, 'student', 15);
INSERT INTO "main"."User_userinfo" VALUES (14, '张三2', 18329126326, 'student', 16);
INSERT INTO "main"."User_userinfo" VALUES (15, '李四1', 18329126326, 'student', 19);
INSERT INTO "main"."User_userinfo" VALUES (16, '李四2', 18329126326, 'student', 20);
INSERT INTO "main"."User_userinfo" VALUES (17, '王五1', 18329126326, 'student', 17);
INSERT INTO "main"."User_userinfo" VALUES (18, '王五2', 18329126326, 'student', 18);
INSERT INTO "main"."User_userinfo" VALUES (19, '老师12', 12, 'college', 12);

-- ----------------------------
-- Indexes structure for table Ask_ask
-- ----------------------------
CREATE INDEX "main"."Ask_ask_grade_id_id_34aabf5e"
ON "Ask_ask" ("grade_id_id" ASC);
CREATE INDEX "main"."Ask_ask_pass_id_id_4c86d767"
ON "Ask_ask" ("pass_id_id" ASC);
CREATE INDEX "main"."Ask_ask_user_id_id_6d53b73d"
ON "Ask_ask" ("user_id_id" ASC);

-- ----------------------------
-- Indexes structure for table Ask_audit
-- ----------------------------
CREATE INDEX "main"."Ask_audit_ask_id_id_aff1d81a"
ON "Ask_audit" ("ask_id_id" ASC);
CREATE INDEX "main"."Ask_audit_user_id_id_70850372"
ON "Ask_audit" ("user_id_id" ASC);

-- ----------------------------
-- Indexes structure for table auth_group_permissions
-- ----------------------------
CREATE INDEX "main"."auth_group_permissions_group_id_b120cbf9"
ON "auth_group_permissions" ("group_id" ASC);
CREATE UNIQUE INDEX "main"."auth_group_permissions_group_id_permission_id_0cd325b0_uniq"
ON "auth_group_permissions" ("group_id" ASC, "permission_id" ASC);
CREATE INDEX "main"."auth_group_permissions_permission_id_84c5c92e"
ON "auth_group_permissions" ("permission_id" ASC);

-- ----------------------------
-- Indexes structure for table auth_permission
-- ----------------------------
CREATE INDEX "main"."auth_permission_content_type_id_2f476e4b"
ON "auth_permission" ("content_type_id" ASC);
CREATE UNIQUE INDEX "main"."auth_permission_content_type_id_codename_01ab375a_uniq"
ON "auth_permission" ("content_type_id" ASC, "codename" ASC);

-- ----------------------------
-- Indexes structure for table auth_user_groups
-- ----------------------------
CREATE INDEX "main"."auth_user_groups_group_id_97559544"
ON "auth_user_groups" ("group_id" ASC);
CREATE INDEX "main"."auth_user_groups_user_id_6a12ed8b"
ON "auth_user_groups" ("user_id" ASC);
CREATE UNIQUE INDEX "main"."auth_user_groups_user_id_group_id_94350c0c_uniq"
ON "auth_user_groups" ("user_id" ASC, "group_id" ASC);

-- ----------------------------
-- Indexes structure for table auth_user_user_permissions
-- ----------------------------
CREATE INDEX "main"."auth_user_user_permissions_permission_id_1fbb5f2c"
ON "auth_user_user_permissions" ("permission_id" ASC);
CREATE INDEX "main"."auth_user_user_permissions_user_id_a95ead1b"
ON "auth_user_user_permissions" ("user_id" ASC);
CREATE UNIQUE INDEX "main"."auth_user_user_permissions_user_id_permission_id_14a6b632_uniq"
ON "auth_user_user_permissions" ("user_id" ASC, "permission_id" ASC);

-- ----------------------------
-- Indexes structure for table django_admin_log
-- ----------------------------
CREATE INDEX "main"."django_admin_log_content_type_id_c4bce8eb"
ON "django_admin_log" ("content_type_id" ASC);
CREATE INDEX "main"."django_admin_log_user_id_c564eba6"
ON "django_admin_log" ("user_id" ASC);

-- ----------------------------
-- Indexes structure for table django_content_type
-- ----------------------------
CREATE UNIQUE INDEX "main"."django_content_type_app_label_model_76bd3d3b_uniq"
ON "django_content_type" ("app_label" ASC, "model" ASC);

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "main"."django_session_expire_date_a5c62663"
ON "django_session" ("expire_date" ASC);

-- ----------------------------
-- Indexes structure for table Manage_typechild
-- ----------------------------
CREATE INDEX "main"."Manage_typechild_par_id_id_0f6f2415"
ON "Manage_typechild" ("par_id_id" ASC);

-- ----------------------------
-- Indexes structure for table Manage_typepar
-- ----------------------------
CREATE INDEX "main"."Manage_typepar_par_id_id_194b3e44"
ON "Manage_typepar" ("par_id_id" ASC);

-- ----------------------------
-- Indexes structure for table User_grade
-- ----------------------------
CREATE INDEX "main"."User_grade_college_id_id_2a62e555"
ON "User_grade" ("college_id_id" ASC);

-- ----------------------------
-- Indexes structure for table User_studentinfo
-- ----------------------------
CREATE INDEX "main"."User_studentinfo_grade_id_id_2fb9680b"
ON "User_studentinfo" ("grade_id_id" ASC);

-- ----------------------------
-- Indexes structure for table User_teacherforcollege
-- ----------------------------
CREATE INDEX "main"."User_teacherforcollege_college_id_id_4c13c1a9"
ON "User_teacherforcollege" ("college_id_id" ASC);
CREATE INDEX "main"."User_teacherforcollege_user_id_id_97465a29"
ON "User_teacherforcollege" ("user_id_id" ASC);

-- ----------------------------
-- Indexes structure for table User_teacherforgrade
-- ----------------------------
CREATE INDEX "main"."User_teacherforgrade_grade_id_id_d1051000"
ON "User_teacherforgrade" ("grade_id_id" ASC);
CREATE INDEX "main"."User_teacherforgrade_user_id_id_52e09b96"
ON "User_teacherforgrade" ("user_id_id" ASC);

-- ----------------------------
-- Indexes structure for table User_userforpermission
-- ----------------------------
CREATE INDEX "main"."User_userforpermission_perm_id_id_b0bf1b6d"
ON "User_userforpermission" ("perm_id_id" ASC);
CREATE INDEX "main"."User_userforpermission_user_id_id_6448b65d"
ON "User_userforpermission" ("user_id_id" ASC);
