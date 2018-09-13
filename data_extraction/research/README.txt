There are 100s of medical ontologies. I'm trying to find a nice linkage
between "signs and symptoms" and "diseases and syndromes". Turns out to
be quite difficult to achieve.

These Ontologies are all available in OWL format, XML format or CSV
format.

SYMP - the Symptom ontology
http://purl.bioontology.org/ontology/SYMP
CSV file is in this folder.

Building a Diseases Symptoms Ontology for Medical Diagnosis: An
Integrative Approach - Mohammed, Benlamri, Fong - 2012
These authors link disease and symptoms. Their linkage is available in
this folder as "DSO.owl". See:
http://flash.lakeheadu.ca/~omohamme/DSO.owl

DS-Ontology: A Disease-Symptom Ontology for General Diagnosis Enhancement
I've requested the article via interlibrary loan, can't find any
downloadable info.

Nature article
Human symptoms–disease network
https://www.nature.com/articles/ncomms5212
Article | Published: 26 June 2014
XueZhong Zhou, Jörg Menche, Albert-László Barabási & Amitabh Sharma
The authors mine the medical literature for co-occuring diseases and
symptoms. They create a dataset of 147,978 connections between 322
symptoms and 4,219 diseases. I've downloaded the data files - they all
start with "ncomm". Have a look at ncomms5212-s4.txt. This is the best I
can come up with. The command line:
$grep $"^Cough" ncomms5212-s4.txt
will show give you an example of how we can use the document score to
see how related any symptom is to any disease.
What is nice about this approach is that rather than give us a hard
cutoff it gives us a document similarity score.
