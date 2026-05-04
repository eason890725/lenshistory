#!/bin/bash
sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'lenshistory' AND pid <> pg_backend_pid();"
sudo -u postgres psql -c "DROP DATABASE IF EXISTS lenshistory;"
sudo -u postgres psql -c "CREATE DATABASE lenshistory;"
echo "Database reset complete!"
