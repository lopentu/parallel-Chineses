# HanLPhttp



## Setup HanLP

**Setup hanlp-1.3.4.jar**

1. Download [hanlp-1.3.4-release.zip](https://github.com/hankcs/HanLP/releases/download/v1.3.4/hanlp-1.3.4-release.zip)
2. Extract it, and move **hanlp-1.3.4.jar** into **./lib/**

**Steup dictionary**

1. Download [data-for-1.3.3.zip](https://drive.google.com/open?id=0B1lvF8Hhw1uZTU5SZ29YbXJaUVk)
2. Extract it, and move **data-for-1.3.3** into **./lib/**

**The file structrue should be like this.**

```sh
HanLPhttp/
├── Makefile
├── README.md
├── bin
│   └── ...
├── lib
│   ├── data-for-1.3.3
│   │   └── ...
│   ├── hanlp-1.3.4.jar
│   └── ...
└── src
    └── ...
```



## How to run

```sh
$ cd HanLPhttp/
$ make
$ make run
```



## Configuration

- **Change server port**

Edit **Makefile**

```makefile
# Default port
PORT = 1234
```

