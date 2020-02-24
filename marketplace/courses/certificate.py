def get_template(student_name, course_name, date, id, tutor_name):
  return """
\documentclass[16pt,a4paper]{scrartcl} %class
\\usepackage[landscape,left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry} %for layout
\\usepackage{setspace} % for spacing between lines
\\usepackage{eso-pic} %package for including background image
\\usepackage{color}

\definecolor{a}{rgb}{0,0.08,0.45}

\definecolor{red}{rgb}{0.5,0,0}

\def\signature#1#2{\parbox[b]{1in}{\smash{#1}\\vskip12pt}
\hfill \parbox[t]{2.8in}{\shortstack{\\vrule width 2.8in height 0.4pt\\\\\small#2}}}
\def\sigskip{\\vskip0.4in plus 0.1in}
\def\\beginskip{\\vskip0.5875in plus 0.1in}
%=============================
\\begin{document}
\\noindent

\hfill
{\centering
{\onehalfspacing
{\LARGE\\bfseries\color{a}EduMarketplace}\\\\
}}
\hfill
\hfill

\\noindent
\hfill
\hfill
\hfill

\\vspace{4cm}
\doublespacing
\\noindent{{\\bfseries This is to certify that student """+student_name+""" has successfully completed the course """+course_name+""".
\\\\Date: """+date+"""
\\\\ Certificate Identification Number: """+id+"""
}}

\\noindent
{\singlespacing

\sigskip \signature{}
{\\bfseries\color{a} """+tutor_name+""" \\\\ \\bfseries\color{a} Tutor }
}

\end{document}
"""
