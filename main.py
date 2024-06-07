from GenetiqueAlgorithms.GenetiqueAlgorithms import genetique_algo

if __name__ == "__main__":
    population_size = 20
    input_size=11*11
    hidden_size=10 # you can change this
    output_size= 4
    num_generations= 50# you can change this
    num_parents= 5# you can change this
    name_fichier= "test1AG"# you can change this
    
    genetique_algo(population_size,input_size,hidden_size,output_size,num_generations,num_parents,name_fichier)
    print("FINISH")