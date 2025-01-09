# Define variables for Python interpreter and script name
PYTHON = python3
SCRIPT = gatorTicketMaster.py

# Define phony targets to prevent conflicts with files of the same name
.PHONY: all run clean

# Default target that provides usage information
all:
	@echo "Use 'make run INPUT=<input_file>' to execute the program."

# Run target that executes the Python script with an input file
run:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: Please specify an input file using 'make run INPUT=<input_file>'"; \
		exit 1; \
	fi
	$(PYTHON) $(SCRIPT) $(INPUT)

# Clean target for removing output files
clean:
	@echo "Cleaning up..."
	@rm -f *_output_file.txt