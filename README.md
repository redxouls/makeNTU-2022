# Magic Bike

## Installation

**Install packages for python library**

```bash
$ pip3 install -r requirements.txt
```

**Install npm packages**

```bash
$ npm install
```

## How to run

**Build the frontend first**

```bash
$ npm run build
```

**Start mqtt broker**

```bash
$ cd src
$ sudo docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/
```

**Start the backend server**

```bash
$ cd src
$ sudo python3 mapbox.py
```

## How to use

You can access the website according to the ip of your computer.
