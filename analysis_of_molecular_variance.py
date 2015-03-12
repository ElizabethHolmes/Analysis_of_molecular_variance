#!/usr/bin/env python

# dealing with command line input
import sys
file = open(sys.argv[1])

# reading information from file
populations = []
allele_profiles = []
delimiter = '\t'
for line in file:
	split = line.rstrip().split(delimiter)
	population = split[0]
	populations.append(population)
	alleles = split[1:]
	allele_profiles.append(alleles)
file.close()

# making an array of the populations	
different_populations = []
for population in populations:
	if population not in different_populations:
		different_populations.append(population)

# writing file headers
output = open('PhiPT_matrix.txt', 'w')
output.write('PhiPT matrix' + '\n\t')
for different_population in different_populations:
	output.write(different_population + '\t')
output.write('\n')

population_list = different_populations

# calculating pairwise PhiPT values
total_populations = 2
PhiPTs = []
for i in range(len(different_populations)-1):
	pop_PhiPTs = ['-']
	pop1 = different_populations[i]
	index = i + 1
	while index < len(different_populations):
		pop2 = different_populations[index]
		population_list = [pop1, pop2]
		allele_profiles = []
		populations = []
		file = open(sys.argv[1])
		for line in file:	
			if line.startswith(different_populations[i]) or line.startswith(different_populations[index]):
				split = line.rstrip().split(delimiter)
				alleles = split[1:]
				allele_profiles.append(alleles)
				population = split[0]
				populations.append(population)
		PhiPT = findPhiPT()
		pop_PhiPTs.append(PhiPT)
		index = index + 1
		file.close()
	PhiPTs.append(pop_PhiPTs)

# calculating overall PhiPT value
total_populations = len(different_populations)
overall_PhiPT = findPhiPT()

# writing pairwise PhiPT values to file
for i in range(len(different_populations)-1):
	output.write(different_populations[i] + '\t')
	for x in range(0,i+1):
		PhiPT_list = PhiPTs[x]
		output.write(str(PhiPT_list[i-x]) + '\t')
	PhiPT_list = PhiPTs[i]
	for x in range(1,len(different_populations)-i):
		output.write(str(PhiPT_list[x]) + '\t')
	output.write('\n')

output.write(different_populations[len(different_populations)-1] + '\t')
for x in range(0,len(different_populations)-1):
	PhiPT_list = PhiPTs[x]
	output.write(str(PhiPT_list[len(different_populations)-x-1]) + '\t')
output.write('-' + '\n\n')

# writing overall PhiPT value to file
output.write('Overall PhiPT:' + '\t' + str(overall_PhiPT))

# function for calculating PhiPT
def findPhiPT():
	differences_matrix = []
	for i in range(len(allele_profiles)-1):
		sample_differences = [0]
		profile = allele_profiles[i]
		index = i + 1
		while index < len(allele_profiles):	
			next_profile = allele_profiles[index]
			differences = 0
			for x in range(len(profile)):
				if not profile[x] == next_profile[x]:
					differences = differences + 1
			sample_differences.append(differences)
			index = index + 1
		differences_matrix.append(sample_differences)
	differences_matrix.append([0])

	SSTOT = 0
	for i in range(len(differences_matrix)):
			differences = differences_matrix[i]
			for x in range(len(differences)):
					SSTOT = SSTOT + differences[x]
	
	SSTOT = float(SSTOT)/float(len(allele_profiles))				
	
	SSWP_each = 0
	SSWP_divisor = 0
	SSWP = 0
	for population in population_list:
		SSWP_each = 0
		SSWP_divisor = 0
		for i in range(len(differences_matrix)):
			differences = differences_matrix[i]
			for x in range(len(differences)):
				if populations[i] == populations[x+i] == population:
					SSWP_each = SSWP_each + differences[x]
					SSWP_divisor = SSWP_divisor + 1
		SSWP_divisor = (2*SSWP_divisor+0.25)**0.5 - 0.5
		SSWP = float(SSWP) + float(SSWP_each)/float(SSWP_divisor)
		
	SSAP = SSTOT - SSWP
		
	squared_count_sum = 0
	for different_population in different_populations:
		count = 0
		for population in populations:
			if population == different_population:
				count = count + 1
		squared_count_sum = squared_count_sum + count**2
	squared_count_sum = float(squared_count_sum)

	total_samples = float(len(allele_profiles))
	total_pops = float(total_populations)
	dfAP = total_populations - 1
	dfWP = len(allele_profiles) - total_populations
	MSAP = float(SSAP/dfAP)
	MSWP = float(SSWP/dfWP)
	N0 = float((total_samples - float(squared_count_sum/total_samples)) * float(1/(total_pops-1)))
	VAP = float((MSAP - MSWP)/N0)
	if VAP + MSWP == 0:
		PhiPT = 0
	else:
		PhiPT = float(VAP/(VAP + MSWP))
	return PhiPT;
