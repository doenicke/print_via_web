# print_via_web

Mini Web-Server zum Hochladen von Dateien, um diese dann
an den Standarddrucker (via lp/CUPS) zu schicken. 

Hintergrund: Fehlende Druckfunktion von Smartphones und Tablets


## Installation

    git clone ...
    cd http-upload
    mkdir uploads
    
Den secret key in `app.py` ändern.    
    
### .service Datei

Als erstes muss eine `.service`-Datei unter `/etc/systemd/system` angelegt werden, 
z.B. mit dem Dateinamen `http-upload.service`. 

    [Unit]
    Description=File upload server with print function

    [Service]
    Type=simple
    ExecStart=/home/BENUTZER/http-upload/app.py

    [Install]
    WantedBy=multi-user.target

Service Unit aktivieren

    sudo systemctl enable http-upload.service 

Anschließend kann die Unit gestartet werden:

    sudo systemctl start http-upload.service 
