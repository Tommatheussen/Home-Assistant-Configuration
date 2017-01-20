#!/bin/bash

echo "http_password: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "google_secret: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "pushbullet_api: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "lastfm_api: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "lastfm_user: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "owm_api: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "mqtt_pass: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "mqtt_username: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "ssl_key: ssl_key.pem" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "ssl_cert: ssl_cert.pem" >> $TRAVIS_BUILD_DIR/secrets.yaml
echo "db_url: dummy" >> $TRAVIS_BUILD_DIR/secrets.yaml
touch "ssl_key.pem"
touch "ssl_cert.pem"
