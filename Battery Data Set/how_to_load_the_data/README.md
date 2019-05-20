The data provided by Nasa is in the .mat format. This is a matlab file format. Matlib files cannot opened directly (even within matlab).
The matlab file format is incompatible with the most used programs for data analysis.  
It is easy to examine matlab files with octave, which can downloaded for free.
More information about this format can be found on :  
  
  https://www.mathworks.com/help/pdf_doc/matlab/matfile_format.pdf
  
  
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html
  
  it is a pretty boring task to convert .mat files into somewhat useful
  
  the program here is still under development, it expects all files you want to extract in the data folder
  the extraction takes time and the data-space explodes
  the files need extracted up to 2 times more space
  
  code works but needs improvement, some statistical fields are missing. it's not pretty formated and code is to complicated
