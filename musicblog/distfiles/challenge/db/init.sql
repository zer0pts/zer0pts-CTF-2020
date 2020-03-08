CREATE TABLE `user` (
  `id` INTEGER AUTO_INCREMENT,
  `username` VARCHAR(256) UNIQUE NOT NULL,
  `password` TEXT NOT NULL,
  `is_admin` TINYINT(1),
  PRIMARY KEY (`id`)
);
CREATE TABLE `post` (
  `id` VARCHAR(256) NOT NULL,
  `username` TEXT NOT NULL,
  `title` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `likes` INTEGER DEFAULT 0,
  `published` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id`)
);

INSERT INTO `user` (`username`, `password`, `is_admin`) VALUES (
  'admin',
  '<censored>',
  1
);
INSERT INTO `post` (`id`, `username`, `title`, `content`, `likes`, `published`) VALUES (
  '00000000-0000-0000-0000-000000000000',
  'admin',
  'Daisy Bell',
  'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. [[/static/song/daisy_bell.mp3]]',
  0,
  1
);
