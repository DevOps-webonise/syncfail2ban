# Readme

## Dev Environment

- Install pip and pipenv to install required packages.
- Built using python v3.5

## Running Commands

```
# Run the daemon
python ./daemon.py -c=/opt/syncfail2ban/config/config.yml

# Run the daemon as master server (master does clean up job)
python ./daemon.py -c=/opt/syncfail2ban/config/config.yml -m

# Ban an IP (this ties in with fail2ban banaction hook)
python ./ban.py -c=/opt/syncfail2ban/config/config.yml -j=[jail] -i=[ip]

```

