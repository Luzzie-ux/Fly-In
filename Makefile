# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rodrpere <rodrpere@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/11/26 22:11:30 by rodrpere          #+#    #+#              #
#    Updated: 2026/11/26 22:46:22 by rodrpere         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

UV = uv
INTERPRETER = python3
DEBUGGER = pdb
RM_DIRS = __pycache__ .mypy_cache

LINTER = flake8 .
TYCHECK = mypy .
TYFLAGS = --warn-return-any \
		  --warn-unused-ignores \
		  --ignore-missing-imports \
		  --disallow-untyped-defs \
		  --check-untyped-defs
install:
	$(UV) sync

run:
	$(INTERPRETER) -m fly-in

debug:
	$(UV) run $(DEBUGGER)

clean:
	@rm -rf $(RM_DIRS)

lint:
	$(UV) run $(LINTER)
	$(UV) run $(TYCHECK) $(TYFLAGS)

lint-strict: TYFLAGS = --strict
lint-strict: lint
