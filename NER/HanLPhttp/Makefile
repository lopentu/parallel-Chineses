# Modify from Makefile author: Joseph Anderson <jtanderson@ratiocaeli.com>

# This is where you specify the necessary source files

# Program packages and files
#   - The packages should be the path inside your src directory. eg: package1 package2/package3
PACKAGES = ntu/ltcl/hanlp

# Java compiler
JAVAC = javac

# Directory for compiled binaries
# - trailing slash is important!
BIN = ./bin/

# Directory of library classes
# - trailing slash is important!
LIB = ./lib/

# Directory of source files
# - trailing slash is important!
SRC = ./src/

# File of JAR library
JAR = ./lib/hanlp-1.3.4.jar

# Java compiler flags
JAVAFLAGS = -g -d $(BIN) -cp "$(BIN):$(LIB):$(SRC):$(JAR)"

# Creating a .class file
COMPILE = $(JAVAC) $(JAVAFLAGS)

EMPTY =

JAVA_FILES = $(subst $(SRC), $(EMPTY), $(wildcard $(SRC)*.java))

ifdef PACKAGES
PACKAGEDIRS = $(addprefix $(SRC), $(PACKAGES))
PACKAGEFILES = $(subst $(SRC), $(EMPTY), $(foreach DIR, $(PACKAGEDIRS), $(wildcard $(DIR)/*.java)))
ALL_FILES = $(PACKAGEFILES) $(JAVA_FILES)
else
ALL_FILES = $(JAVA_FILES)
endif

# One of these should be the "main" class listed in Runfile
CLASS_FILES = $(ALL_FILES:.java=.class)

all: $(addprefix $(BIN), $(CLASS_FILES))

# The line describing the action starts with <TAB>
$(BIN)%.class: $(SRC)%.java
	$(COMPILE) $<

.PHONY: clean

clean:
	rm -rf $(BIN)*

run:
	java -cp "./:$(BIN):$(LIB):$(JAR)" ntu/ltcl/hanlp/HanLPhttp
