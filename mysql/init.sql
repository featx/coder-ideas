create schema `coder` default char set utf8mb4 collate utf8mb4_unicode_ci;
create user `coder`@'%' identified by 'coder';
grant all on coder.* to `coder`@'%';
use coder;
create table if not exists `t_coder_language`
(
    `id`         bigint unsigned  not null auto_increment comment 'id for index',
    `code`       varchar(16)      not null default '' comment '编程语言编码',
    `name`       varchar(64)      not null default '' comment '编程语言名称',
    `comment`    varchar(1024)    not null default '' comment '备注，说明等',
    `deleted`    tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at` datetime         not null default current_timestamp comment '创建时间',
    `updated_at` datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment '编程语言';

create unique index `unq_language_code` on `t_coder_language` (`code`);

create table if not exists `t_coder_framework`
(
    `id`         bigint unsigned  not null auto_increment comment 'id for index',
    `code`       varchar(16)      not null default '' comment '编程框架编码',
    `name`       varchar(64)      not null default '' comment '编程框架名称',
    `alias`      varchar(32)      not null default '' comment '编程框架简称',
    `comment`    varchar(1024)    not null default '' comment '备注，说明等',
    `deleted`    tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at` datetime         not null default current_timestamp comment '创建时间',
    `updated_at` datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment '编程框架';
create unique index `unq_framework_code` on `t_coder_framework` (`code`);

create table if not exists `t_coder_data_engine`
(
    `id`         bigint unsigned  not null auto_increment comment 'id for index',
    `code`       varchar(16)      not null default '' comment '数据引擎 编码',
    `name`       varchar(64)      not null default '' comment '模块 名称',
    `type`       int unsigned     not null default 0 comment '数据引擎类型，0关系,1搜索,2文档',
    `sort`       int unsigned     not null default 0 comment '模块 排序位 默认为0',
    `image_url`  varchar(128)     not null default '' comment '模块 图示 url',
    `comment`    varchar(1024)    not null default '' comment '备注，说明等',
    `deleted`    tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at` datetime         not null default current_timestamp comment '创建时间',
    `updated_at` datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment '支持的数据存储类型';
create unique index `unq_data_engine_code` on `t_coder_data_engine` (`code`);
create index `idx_data_engine_image_url` on `t_coder_data_engine` (`image_url`);

create table if not exists `t_coder_project`
(
    `id`                 bigint unsigned  not null auto_increment comment 'id for index',
    `code`               varchar(16)      not null default '' comment '开发项目 编码',
    `name`               varchar(64)      not null default '' comment '开发项目 名称',
    `type`               int unsigned     not null default 0 comment '项目类型',
    `status`             int unsigned     not null default 0 comment '项目状态',
    `image_url`          varchar(128)     not null default '' comment '开发项目 logo',
    `language_code`      varchar(16)      not null default '' comment '所用开发语言编码',
    `framework_code`     varchar(16)      not null default '' comment '所用框架参照编码',
    `template_repo_url`  varchar(128)     not null default '' comment '模板开发VCS库地址',
    `template_api_token` varchar(128)     not null default '' comment '模板项目库地址的api_token',
    `repo_url`           varchar(128)     not null default '' comment '当前项目自己的VCS库地址',
    `api_token`          varchar(128)     not null default '' comment '访问自己项目库地址的api_token',
    `comment`            varchar(255)     not null default '' comment '备注，说明等',
    `deleted`            tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at`         datetime         not null default current_timestamp comment '创建时间',
    `updated_at`         datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment 'vcs库单位 开发项目';

create unique index `unq_project_code` on `t_coder_project` (`code`);
create index `idx_project_image_url` on `t_coder_project` (`image_url`);
create index `idx_project_language_code` on `t_coder_project` (`language_code`);
create index `idx_project_framework_code` on `t_coder_project` (`framework_code`);
create index `idx_project_template_repo_url` on `t_coder_project` (`template_repo_url`);
create index `idx_project_template_api_token` on `t_coder_project` (`template_api_token`);
create index `idx_project_repo_url` on `t_coder_project` (`repo_url`);
create index `idx_project_api_token` on `t_coder_project` (`api_token`);

create table if not exists `t_coder_project_domain`
(
    `id`           bigint unsigned  not null auto_increment comment 'id for index',
    `code`         varchar(16)      not null default '' comment '项目某个域 的编码',
    `name`         varchar(64)      not null default '' comment '域 名称',
    `type`         int unsigned     not null default 0 comment '域类型 0日志,1可维护2标准',
    `sort`         int unsigned     not null default 0 comment '模块 排序位 默认为0',
    `project_code` varchar(16)      not null default '' comment '域所属项目 的编码',
    `comment`      varchar(1024)    not null default '' comment '备注，说明等',
    `deleted`      tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at`   datetime         not null default current_timestamp comment '创建时间',
    `updated_at`   datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment '开发项目中的领域模型';
create unique index `unq_project_domain_code` on `t_coder_project_domain` (`code`);
create index `idx_project_domain_project_code` on `t_coder_project_domain` (`project_code`);

create table if not exists `t_coder_domain_property`
(
    `id`           bigint unsigned  not null auto_increment comment 'id for index',
    `code`         varchar(16)      not null default '' comment '项目某域的一个属性 的编码',
    `name`         varchar(64)      not null default '' comment '属性 名称',
    `type`         int unsigned     not null default 0 comment '域属性类型 按照项目编程语言确定',
    `sort`         int unsigned     not null default 0 comment '模块 排序位 默认为0',
    `domain_code`  varchar(16)      not null default '' comment '属性所属域 的编码',
    `project_code` varchar(16)      not null default '' comment '域所属项目  的编码',
    `comment`      varchar(1024)    not null default '' comment '备注，说明等',
    `deleted`      tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at`   datetime         not null default current_timestamp comment '创建时间',
    `updated_at`   datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment '领域属性';
create unique index `unq_domain_property_code` on `t_coder_domain_property` (`code`);
create index `idx_domain_property_project_code` on `t_coder_domain_property` (`project_code`);
create index `idx_domain_property_domain_code` on `t_coder_domain_property` (`domain_code`);

create table if not exists `t_coder_project_data_engine`
(
    `id`               bigint unsigned  not null auto_increment comment 'id for index',
    `code`             varchar(16)      not null default '' comment '数据引擎 编码',
    `data_engine_code` varchar(64)      not null default '' comment '模块 名称',
    `project_code`     int unsigned     not null default 0 comment '数据引擎类型，0关系,1搜索,2文档',
    `sort`             int unsigned     not null default 0 comment '模块 排序位 默认为0',
    `comment`          varchar(1024)    not null default '' comment '备注，说明等',
    `deleted`          tinyint unsigned not null default 0 comment '软删除标示:0否1是',
    `created_at`       datetime         not null default current_timestamp comment '创建时间',
    `updated_at`       datetime         not null default current_timestamp on update current_timestamp comment '更新时间',
    primary key (`id`) using btree
) engine = InnoDB comment '项目中所使用的数据引擎';

create unique index `unq_project_data_engine_code` on `t_coder_project_data_engine` (`code`);
create index `idx_project_data_engine_data_engine_code` on `t_coder_project_data_engine` (`data_engine_code`);
create index `idx_project_data_engine_project_code_code` on `t_coder_project_data_engine` (`project_code`);
