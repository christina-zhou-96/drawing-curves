# set paths here
ATS_path = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\ATS Analysis'
Word_path = ATS_path + "\\" + "Raw Analysis"

# include downloads and their header rows to analyze here
dls_to_analyze = [
    ("RSBS",3),
    ("RLBS",3),
    ("RCSR",3),
    ("EMSD",5),
    ("EMSC",3),
    ("RLTE",2),
    ("RCSD",4),
                ]

# dictionary with the download and its respective filename
dls_to_analyze_dict = {dl[0]: ("\\" + dl[0] + ".csv", dl[1]) for dl in dls_to_analyze}
