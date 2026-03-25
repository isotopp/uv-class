BOOK_DIR := content/books/uv-class
OUT_DIR := out
BUILD_DIR := $(OUT_DIR)/build
BOOK_BUILD_DIR := $(BUILD_DIR)/uv-class
BOOK_MD := $(BUILD_DIR)/uv-class.md
BOOK_FILES := $(BOOK_DIR)/_index.md $(sort $(wildcard $(BOOK_DIR)/*/_index.md))
PANDOC := pandoc
PANDOC_FLAGS := --standalone --toc --resource-path="$(BUILD_DIR)" --metadata title="Using uv to manage Python projects" --metadata author="Kristian Köhntopp"

.PHONY: all clean

all: $(OUT_DIR)/uv-class.epub $(OUT_DIR)/uv-class.docx $(OUT_DIR)/uv-class.odt $(OUT_DIR)/uv-class.html

clean:
	rm -rf "$(OUT_DIR)"

$(OUT_DIR):
	mkdir -p "$(OUT_DIR)"

$(BOOK_MD): $(BOOK_FILES) | $(OUT_DIR)
	python3 scripts/render_book.py --source "$(BOOK_DIR)" --build-dir "$(BOOK_BUILD_DIR)" --output "$@"

$(OUT_DIR)/uv-class.epub: $(BOOK_MD)
	$(PANDOC) $(PANDOC_FLAGS) -o "$@" "$<"

$(OUT_DIR)/uv-class.docx: $(BOOK_MD)
	$(PANDOC) $(PANDOC_FLAGS) -o "$@" "$<"

$(OUT_DIR)/uv-class.odt: $(BOOK_MD)
	$(PANDOC) $(PANDOC_FLAGS) -o "$@" "$<"

$(OUT_DIR)/uv-class.html: $(BOOK_MD)
	$(PANDOC) $(PANDOC_FLAGS) -o "$@" "$<"
