# Analysis_of_molecular_variance
## About
Analysis_of_molecular_variance is a Python script for performing an analysis of molecular variance (AMOVA). AMOVA is a statistical technique developed by [Excoffier *et al.* (1992)](http://www.genetics.org/content/131/2/479.short) to determine differences between different populations of a species.

For example, AMOVA could be used to determine how closely related bacterial populations collected from different countries are, from which inferences could be made about how the bacteria have spread.

## Citation
Analysis_of_molecular_variance is not associated with a paper; to cite it please use:

    Sutton, ER. (2015). Analysis_of_molecular_variance [Software]. 
    Available at https://github.com/ElizabethSutton/Analysis_of_molecular_variance.

## Requirements
Analysis_of_molecular_variance requires Python.

## Usage
Analysis_of_molecular_variance takes as its input a tab-delimited text file, such as the 'bacterial_populations.txt' file provided, comprising a list of samples, with the leftmost column containing the population name for each sample (e.g. the country from which the sample was derived). There can be any number of different populations. The remaining columns, of which there may be any number, contain assignments for categorical characteristics of the sample (e.g. MLST allele numbers). The example input file provided, 'bacterial_populations.txt', looks like this:

 | | | |
--- | --- | --- | ---
UK | gene1:allele1 | gene2:allele1 | gene3:allele4
UK | gene1:allele1 | gene2:allele1 | gene3:allele3
USA | gene1:allele2 | gene2:allele2 | gene3:allele1
USA | gene1:allele2 | gene2:allele1 | gene3:allele4
Australia | gene1:allele3 | gene2:allele3 | gene3:allele2
Australia | gene1:allele2 | gene2:allele3 | gene3:allele4 

### *Example*
To calculate the difference between the bacterial populations described in the example input file provided, 'bacterial_populations.txt', the command would be:

    ./analysis_of_molecular_variance.py bacterial_populations.txt

## Output
Analysis_of_molecular_variance calculates a total score for every possible pairwise comparison of samples in the dataset, with a score of 1 being given for every characteristic in which the samples differ. The average difference between populations is then compared to the average difference within populations, and a measure known as PhiPT returned to indicate the level of difference between populations. A PhiPT value of 0 suggests that there is no difference between populations, while a PhiPT value of 1 suggests that populations are completely distinct. A negative PhiPT value suggests that samples within a population are more closely related to samples from another population than they are to samples within their own population.

The output of the script is a text file containing a table of PhiPT values for every pairwise comparison of populations within the dataset, followed by a PhiPT value for all populations compared together.
