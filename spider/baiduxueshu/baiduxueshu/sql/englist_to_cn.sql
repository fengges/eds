/*
Navicat MySQL Data Transfer

Source Server         : 本地mysql
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : schoollink

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-07-02 22:18:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for englist_to_cn
-- ----------------------------
DROP TABLE IF EXISTS `englist_to_cn`;
CREATE TABLE `englist_to_cn` (
  `id` varchar(50) NOT NULL,
  `cn` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
