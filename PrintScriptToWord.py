import RunSummaryStats
import io
import sys
from docx import Document

# collect data for word
def print_word(filepath, filename, header, word_filepath, word_filename):
    print(filepath + "\\" + word_filename)
    orig_stdout = sys.stdout
    stat_buffer = io.StringIO()
    sys.stdout = stat_buffer
    try:
        RunSummaryStats.run_summary(filepath, filename, header)
    finally:
        sys.stdout = orig_stdout
    document = Document()
    document.add_paragraph(stat_buffer.getvalue())
    document.save(word_filepath + "\\" + word_filename)
