import RunSummaryStats
import io
import sys
from docx import Document

# put together tuples of information here
SSD_COORD_INFO = (r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\SSD Coordinator and Requests',
           r'\NYCDOE SSD Coordinator and Request Report_20190808.xlsx',
           [0,1],
           r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\Auto Analysis',
           'SSD Coordinator Auto Analysis.docx',
            0)

SSD_COORD_2021_INFO = (r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\SSD Coordinator and Requests',
           r'\NYCDOE SSD Coordinator and Request Report_20190808.xlsx',
           [0,1],
           r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\Auto Analysis',
           'SSD Coordinator 2021 Auto Analysis.docx',
            3)

SAT_COORD_INFO = (r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\SAT Coordinators'
                  ,
                  r'\PSAT_SAT Coordinator List - July 2019.xlsx',
                  [0,1],
                    r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\Auto Analysis',
                    'SAT Coordinator Auto Analysis.docx',
                  0
                  )

FALL_ORDERS_INFO = (r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\Ordering - Fall 2019'
                  ,
                  r'\NYCDOE Fall Orders_20190719.xlsx',
                  [0,1],
                    r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\College Board\2019-20 SAT School Day Initiative\01 - Data\CB Weekly Reports\Auto Analysis',
                    'Fall Orders Auto Analysis.docx',
                  0
                  )

# collect data for word
def print_word(filepath, filename, header, word_filepath, word_filename, sheet):
    print(filepath + "\\" + word_filename)
    orig_stdout = sys.stdout
    stat_buffer = io.StringIO()
    sys.stdout = stat_buffer
    try:
        RunSummaryStats.run_summary(filepath, filename, header, sheet)
    finally:
        sys.stdout = orig_stdout
    document = Document()
    document.add_paragraph(stat_buffer.getvalue())
    document.save(word_filepath + "\\" + word_filename)

# unpack each specific tuple argument here
print_word(*FALL_ORDERS_INFO)


