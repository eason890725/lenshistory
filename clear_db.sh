#!/bin/bash
sudo -u postgres psql -d lenshistory -c 'DELETE FROM gear_mounts; DELETE FROM gears; DELETE FROM i18n_strings; DELETE FROM brands; DELETE FROM mounts;'
echo "Database cleared!"
