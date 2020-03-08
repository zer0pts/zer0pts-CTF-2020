FROM php:7.3-apache

ADD challenge/index.php /var/www/html/
ADD challenge/recaptcha.php /var/www/html/
ADD challenge/assets/patternlock.css /var/www/html/assets/
ADD challenge/assets/patternlock.js /var/www/html/assets/

RUN chown -R www-data:www-data /var/www/
