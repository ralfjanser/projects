

__Notebook Extensions__  
Installation with conda:  

conda install -c conda-forge jupyter_nbextensions_configurator  
  
Or with pip:  
  
pip install jupyter_contrib_nbextensions && jupyter contrib  
nbextension install  
  
#incase you get permission errors on MacOS,  
  
pip install jupyter_contrib_nbextensions && jupyter contrib  
nbextension install --user  
  

__Plotly Cufflinks__  
  
pip install plotly # Plotly is a pre-requisite before installing cufflinks  
pip install cufflinks  



__pandas_profiling__

has currently to be installed manually

git clone https://github.com/pandas-profiling/pandas-profiling

cd pandas profiling

From source

Download the source code by cloning the repository or by pressing 'Download ZIP' on this page. Install by navigating to the proper directory and running

python setup.py install


*pip and conda install the wrong version*
