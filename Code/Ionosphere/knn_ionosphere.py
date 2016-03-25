import csv
import random, math
import matplotlib.pyplot as plt

def get_dist(var1, var2, dimensions):
	dist=0
	for i in range(dimensions):
		dist+=pow((var1[i]-var2[i]), 2)
	return math.sqrt(dist)

def partition(file_name, train_set=[], test_set=[], split_value=0.5):
	data = []

	with open(file_name, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			for j in range(len(row)-1):
				row[j]=float(row[j])
			data.append(row)

	random.shuffle(data)

	length = int(len(data)*split_value)

	train_set=data[:length]
	test_set=data[length:]

	return train_set, test_set

def k_fold(file_name, k_value=5):
	data = []

	with open(file_name, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			for j in range(len(row)-1):
				row[j]=float(row[j])
			data.append(row)

	random.shuffle(data)

	avg = len(data) / float(k_value)
	out = []
	last = 0.0
	
	while last < len(data):
		out.append(data[int(last):int(last + avg)])
		last += avg

  	return out

def KNN(train_set, test_instance, k):
	dists = []
	dimensions = len(test_instance) - 1
	for train_instance in train_set:
		dist = get_dist(train_instance, test_instance, dimensions)
		dists.append([dist, train_instance])

	dists.sort(key=lambda x:x[0])

	nearest_neighbours = []

	for i in range(k):
		nearest_neighbours.append(dists[i][1])

	return nearest_neighbours

if __name__ == '__main__':
	#print 'Running KNN-Algo'

	k_values=[1, 3]
	splitValues = [0.5]
	no_of_iterations = 10

	train_set, test_set = [], []

	confusion_matrix = {}
	row = {}
	keys = ['b', 'g']

	colors = ['r', 'g']
	plot_color = dict(zip(keys, colors))
	
	for key in keys:
		row[key]=0

	for key in keys:
		confusion_matrix[key]=row

	for k_value in k_values:
		print '--------------------------------------------------------------------------	'
		print 'K-Value: ' +  str(k_value)
		accuracy_list = []

		for iteration_no in range(no_of_iterations):
			print '--------------------------------------------------------------------------	'
			for key in confusion_matrix:
				for secondary_key in confusion_matrix[key]:
					confusion_matrix[key][secondary_key]=0

			for key in keys:
				confusion_matrix[key]=row

			print 'Iteration no. ' + repr(iteration_no + 1)
			train_set, test_set = partition('ionosphere.data', train_set, test_set, splitValues[0])
			#train_set, test_set = k_fold('ionosphere.data', train_set, test_set, 5)
			count = 0
			for test_instance in test_set:
				nearest_neighbours = KNN(train_set, test_instance, k_value)
				
				neighbour_count = {}

				for key in nearest_neighbours:
					if neighbour_count.has_key(key[-1]):
						neighbour_count[key[-1]]+=1
					else:
						neighbour_count[key[-1]]=1


				max_count, max = 0, None
				for key in neighbour_count:
					if neighbour_count[key] > max_count:
						max, max_count=key, neighbour_count[key]

				confusion_matrix[max][test_instance[-1]]+=1

				#plt.scatter(test_instance[1], test_instance[3], color=plot_color[test_instance[-1]])

				if max==test_instance[-1]:
					count=count + 1

			#plt.show()

			print 'Confusion Matrix: '
			for key in confusion_matrix:
				print '|', 
				print key,
			print '|'

			for key in confusion_matrix:
				for secondary_key in keys:
					print '|', confusion_matrix[key][secondary_key],
				print '|'

			accuracy = (float(count)/len(test_set)) * 100.0
			accuracy_list.append(accuracy)

		mean = float(sum(accuracy_list)/len(accuracy_list))
		stddev = 0

		for i in range(len(accuracy_list)):
			stddev += pow(float(accuracy_list[i]) - mean, 2)

		stddev = math.sqrt(stddev/len(accuracy_list))

		print '---------------------Iteration ' + repr(i+1) + '--------------------'
		print 'Mean: ' + str(mean)
		print 'Standard Deviation: ' + str(stddev)

	k_fold_div = 5
	mean_list = []

	for k_value in k_values:
		print '--------------------------------------------------------------------------'
		print 'K-Value: ' +  str(k_value)

		accuracy_list = []
		
		for j in range(k_fold_div):
			accuracy_list.append([])

		for iteration_no in range(no_of_iterations):
			print '--------------------------------------------------------------------------	'
			for key in confusion_matrix:
				for secondary_key in confusion_matrix[key]:
					confusion_matrix[key][secondary_key]=0

			for key in keys:
				confusion_matrix[key]=row

			print 'Iteration no. ' + repr(iteration_no + 1)

			sets = k_fold('ionosphere.data', k_fold_div)

			for j in range(k_fold_div):
				test_set = sets[j]
				train_set = []

				for x in range(k_fold_div):
					if x==j:
						continue
					train_set += sets[x]
			
				count = 0
				for test_instance in test_set:
					nearest_neighbours = KNN(train_set, test_instance, k_value)
					
					neighbour_count = {}

					for key in nearest_neighbours:
						if neighbour_count.has_key(key[-1]):
							neighbour_count[key[-1]]+=1
						else:
							neighbour_count[key[-1]]=1


					max_count, max = 0, None
					for key in neighbour_count:
						if neighbour_count[key] > max_count:
							max, max_count=key, neighbour_count[key]

					confusion_matrix[max][test_instance[-1]]+=1

					if max==test_instance[-1]:
						count=count + 1

				print 'Confusion Matrix: '
				for key in confusion_matrix:
					print '|', 
					print key,
				print '|'

				for key in confusion_matrix:
					for secondary_key in keys:
						print '|', confusion_matrix[key][secondary_key],
					print '|'

				accuracy = (float(count)/len(test_set)) * 100.0
				#print accuracy
				accuracy_list[j].append(accuracy)
				#for i in len()

			mean = 0
			for y in range(k_fold_div):
				mean+=accuracy_list[y][-1]
			mean = mean / float(k_fold_div)
			mean_list.append(mean)

			stddev = 0
			for i in range(k_fold_div):
				stddev += pow(float(accuracy_list[i][-1]) - mean, 2)

			stddev = math.sqrt(stddev/float(k_fold_div))

			print '---------------------Iteration ' + repr(iteration_no+1) + '--------------------'
			print 'Mean: ' + str(mean) + '%'
			print 'Standard Deviation: ' + str(stddev)

		for j in range(k_fold_div):
			plt.plot( range(1, no_of_iterations + 1), 
				accuracy_list[j], 's-', 
				label='Fold no.: ' + str(j + 1) + str(' ,K: ') + str(k_value))


		mean = float(sum(mean_list)/len(mean_list))
		print '---------------------K: ' + repr(k_value) + '--------------------'
		print 'Grand Mean: ' + str(mean) + '%'

		#for i in range(k_fold_div):
		#	plt.plot(range(1, len(accuracy_list)/ 5 + 1), sets[i], 'o-', label='partition no.: ' + str(i+1))
		
		plt.legend(loc='best', fancybox=True)

		plt.show()
