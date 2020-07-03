--用户表
create table user
(id int primary key auto_increment,
first_name varchar(100),
last_name varchar(100),
login varchar(80),
email varchar(120),
password varchar(64));

alter table user add unique index idx_login (login);

--理财渠道表
 CREATE TABLE `myweb`.`fchannel` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键列',
  `channelname` VARCHAR(45) NOT NULL COMMENT '渠道名称',
   `info` varchar(255) DEFAULT NULL COMMENT '说明',
   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   `is_deleted` int DEFAULT NULL DEFAULT 1,
   `delete_time` bigint DEFAULT NULL,
   `uuid` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '理财渠道表';

--理财类型表
CREATE TABLE `myweb`.`ftype` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键列',
  `typename` VARCHAR(45) NOT NULL COMMENT '类型名称',
   `info` varchar(255) DEFAULT NULL COMMENT '说明',
   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   `is_deleted` int DEFAULT NULL DEFAULT 1,
   `delete_time` bigint DEFAULT NULL,
   `uuid` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '理财类型表';

ALTER TABLE `myweb`.`ftype`
ADD UNIQUE INDEX `typename_UNIQUE` (`typename` ASC) VISIBLE;

--理财明细表
CREATE TABLE `myweb`.`finfo` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键列',
  `channelid` INT NOT NULL COMMENT '渠道ID',
  `typeid` INT NOT NULL COMMENT '类型ID',
  `fundname` varchar(255) DEFAULT NULL COMMENT '基金名称',
  `amount` DECIMAL(5,2) DEFAULT NULL COMMENT '金额',
  `status` varchar(255) DEFAULT NULL COMMENT '状态（新购、追加、卖出）',
   `info` varchar(255) DEFAULT NULL COMMENT '说明',
   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   `is_deleted` int DEFAULT NULL DEFAULT 1,
   `delete_time` bigint DEFAULT NULL,
   `uuid` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '理财明细表';

--阅读表

--健身表

