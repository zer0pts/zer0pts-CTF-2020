<?php
require_once 'init.php';

$_SESSION = array();
session_destroy();

header('Location: /');