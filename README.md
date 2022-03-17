# Magic Bike

## Installation

**Install packages for python library**

```bash
$ pip3 install -r requirements.txt
```

**Install npm packages**

```bash
$ yarn
```

## How to run

**Development**

```bash
$ yarn start
```

**Build the frontend first**

```bash
$ yarn build
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
