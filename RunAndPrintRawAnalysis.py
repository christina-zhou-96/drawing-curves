import PrintScriptToWord
import FilesToAnalyze

# select input path here, or where the dl lives
path = FilesToAnalyze.ATS_path

# select output path here, or where to put the raw Word analysis
word_path = FilesToAnalyze.Word_path

# select desired downloads here
for dl,dl_info in FilesToAnalyze.dls_to_analyze_dict.items():
    PrintScriptToWord.print_word(path, dl_info[0], dl_info[1], word_path, dl + " Raw Analysis v2.docx")
