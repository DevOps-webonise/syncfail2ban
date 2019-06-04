# Readme

## Dev Environment

- Tested using python v3.4-3.7. So best to alias python, and pip. For example:

```
#~/.bash_aliases
alias python='python3.7'
alias pip='pip3.7'
```

- Install pip and pipenv and run ```pipenv install``` to install required packages.


## Running Commands

```
# Run the daemon
python ./daemon.py -c=/opt/syncfail2ban/config/config.yml

# Run the daemon as master server (master does clean up job)
python ./daemon.py -c=/opt/syncfail2ban/config/config.yml -m

# Ban an IP (this ties in with fail2ban banaction hook)
python ./ban.py -c=/opt/syncfail2ban/config/config.yml -j=[jail] -i=[ip]

```

