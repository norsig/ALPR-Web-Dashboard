# Automatic License Plate Recognition Web Dashboard

This is a web front end for [OpenALPR](https://github.com/openalpr/openalpr) project. OpenALPR process video streaming looking for plates, once detected, it sends the plate information to this web app to be stored and shown in real time.
This is useful for tolls, patrols and security cameras.

## Installation

 - Download web2py web framework
 - Clone this app under applications folder
 - [Setup IP Cameras in the /etc/alprd.conf and run your OpenALPR process](https://github.com/openalpr/openalpr/wiki) and point the daemon to http://your_web_server_ip/alpr_app/default/call/json/message.
 - From web server command line run: python web2py/gluon/contrib/websocket_messaging.py -k your_websocket_key -p 8888
 - Multiple clients can now connect and receive real time alerts from web browser.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## TODO

This is a really work in process, it works but there's a LOT yet to do.

## Credits

Author: Luciano Laporta Podazza
