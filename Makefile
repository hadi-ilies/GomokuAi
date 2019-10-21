##
## EPITECH PROJECT, 2019
## AIA_gomoku_2019
## File description:
## Build IA
##

NAME = pbrain-gomoku-ai
DIST = .
SRC_DIR = src
SRC_MAIN = main.py
RM = rm
FORCE = -f
RM_RECURSIVE = -r

all: $(NAME)

$(NAME): mouli

mouli:
	ln -s $(FORCE) $(SRC_DIR)/*.py .
	$(RM) $(FORCE) $(SRC_MAIN)
	echo "#!/usr/bin/env python3" > $(NAME)
	cat $(SRC_DIR)/$(SRC_MAIN) >> $(NAME)
	chmod +x $(NAME)

piskvork:
	pip3 install pyinstaller
	pyinstaller -F $(SRC_DIR)/$(SRC_MAIN) -n $(NAME) --distpath $(DIST)

clean:
	$(RM) $(FORCE) $(NAME).spec
	$(RM) $(RM_RECURSIVE) $(FORCE) build
	$(RM) $(RM_RECURSIVE) $(FORCE) $(SRC_DIR)/__pycache__
	$(RM) $(RM_RECURSIVE) $(FORCE) __pycache__
	$(RM) $(FORCE) *.py

fclean: clean
	$(RM) -f $(NAME)

re: fclean all

.PHONY: all $(NAME) fclean re clean mouli piskvork
