# SearchITI
SearchITI allows you to use RipGrep to search the OpenITI corpus [See below for the references].

You have to first download OpenITI on the zenodo platform:
https://doi.org/10.5281/zenodo.6808108 

SearchITI offers two option:
(1) search with RipGrepy, a python module designed to perform searches with RipGrep; or
(2) search with RipGrep directly.

# Search with RipGrepy
Use the function `searchiti.get_grepy` and provide the following parameters:
- search: the string or RegEx (if you search non-Arabic characters) that you want to find in the corpus;
- in_path: the path to the OpenITI folder with the text data (the original folder is called `data`);
- out_path: the path to the folder where you want to save your results;
- format: the format in which you want your results to be printed, 'html' (default) or 'csv'.

# Search with RipGrep
If you want your results to be printed on a .csv file, use `searchiti.rg_to_csv`, if you want the results to be diplayed in an .html file, `searchiti.rg_to_html`.
Both functions require the following parameters:
- out_path: the path to the folder where you want to save your results;
- search: the string or RegEx (if you search non-Arabic characters) that you want to find in the corpus;
- in_path: the path to the OpenITI folder with the text data (the original folder is called `data`);
- cxt: the number of lines around the match that you want to see, 0 (default), 1 or 2.

# References
`OpenITI`
To credit the authors of OpenITI, please use the following citation:
Nigst, Lorenz, Romanov, Maxim, Savant, Sarah Bowen, Seydi, Masoumeh, & Verkinderen, Peter. (2022). OpenITI: a Machine-Readable Corpus of Islamicate Texts (2022.1.6) [Data set]. Zenodo.

`RipGrep`
You will find RipGrep original code on GitHub: https://github.com/BurntSushi/ripgrep.

`RipGrepy`
The implementation of RipGrep for Python can also be found on GitHub: https://github.com/securisec/ripgrepy.
And its documentation is available on ReadTheDocs: https://ripgrepy.readthedocs.io/en/latest/.
To pip install it just go to PyPi: https://pypi.org/project/ripgrepy/.