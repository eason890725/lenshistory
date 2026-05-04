#!/bin/bash
service postgresql start
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"
sudo -u postgres createdb lenshistory
