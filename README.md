# JET

## Install

### Linux / Unix / macOS
```
sudo mkdir /tmp/criexe && sudo mkdir /tmp/criexe/jet && sudo chmod -R 777 /tmp/criexe/jet && sudo curl -o /tmp/criexe/jet/jet http://criexe.com/jet/latest/source.txt && sudo mv /tmp/criexe/jet/jet /usr/local/bin/jet && sudo chmod 755 /usr/local/bin/jet
``` 

### Update JET
```jet update```

### Help & Home Page
```jet```

## Git

### Auto Push
```jet push auto```
To wait for commit message : 
```jet push hold```

### Fast Commit & Push
```jet push "COMMIT MESSAGE"```

### Update base/master
```jet update base```


## Apache

### Apache Restart
```jet apache restart```

### Create New Site
```jet apache create-site [DOMAIN] [PATH]```