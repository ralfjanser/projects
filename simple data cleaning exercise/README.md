
Data cleaning always depends on the dataset and the algorithms you like to use. A data preperation for machine learning can be divided into a simple data cleaning and a data preprocessing.

There is no fixed schema how to do this. Sometimes you'll have to go different ways in data cleaning and preprocessing to hit the best algorithm for your question. There are several methods for data preprocessing, the scikit-learn documentation (http://scikit-learn.org/stable/modules/preprocessing.html) has some information on how to use various different preprocessing methods. You can review the preprocess API in scikit-learn here(http://scikit-learn.org/stable/modules/preprocessing.html). 

For practise I'll use this schema for the data cleaning

-  Feature selection, werden alle Features benötigt, ist hier redundante Information vorhanden? Jedoch sollte hier kein Bias durch eine falsche Datenwahl erzeugt werden  
-  Fehlende Daten (missing data)  
-  Skalierung und Normalisierung der Daten (scaling and normalization)  
-  Analyse der Zeitangaben (parsing dates)  
-  Zeichenkodierung (character encoding)  
-  Inkonsistente Daten (inconsistent data entry)  
