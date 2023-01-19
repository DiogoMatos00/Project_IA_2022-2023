import csv;
import numpy as np;
import math;
from Perceptron import Perceptron;
from timeit import default_timer as timer

# Timer para conseguir regular o tempo de execução do programa em segundos.
# START MY TIMER
start = timer();

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) /len(y_true)
    return accuracy

def getMetrics(y_true, y_pred):
    Metrics = {
        'acc': 0,
        'err': 0,
        'sn': 0,
        'sp': 0,
        'p': 0,
        'r': 0,
        'fm': 0,
        'gm': 0
    }

    tp = np.sum(np.logical_and(y_true == y_pred, y_pred == 1)); #True positive
    tn = np.sum(np.logical_and(y_true == y_pred, y_pred == 0)); #True negative
    fp = np.sum(np.logical_and(y_true != y_pred, y_pred == 1)); #False positive
    fn = np.sum(np.logical_and(y_true != y_pred, y_pred == 1)); #False negative

    Metrics['acc'] = (tp + tn)/(tp + tn + fp + fn);
    Metrics['err'] = (fp + fn)/(tp + tn + fp + fn);
    Metrics['sn'] = tp/(tp+fn);
    Metrics['sp'] = tn/(tn+fp);
    Metrics['p'] = tp/(tp+fp);
    Metrics['r'] = tp/(tp+tn);
    Metrics['fm'] = (2 * Metrics['p'] * Metrics['r'])/(Metrics['p'] + Metrics['r']);
    Metrics['gm'] = math.sqrt(tp * tn);

    return Metrics;

def printMetrics(data: dict):
    print("""

        Metricas para o tratamento de dados com Peceptrão
        ================================
        Accuracy(acc) : {}
        Error Rate(err) : {}
        Sensitivity(sn) : {}
        Specificity(sp) : {}
        Precision(p) : {}
        Recall(r) : {}
        F-Measure(FM) : {}
        Geometric-mean(GM) : {}

    """.format(data['acc'], data['err'], data['sn'], data['sp'], data['p'], data['r'], data['fm'], data['gm']))

def training_data_treatment(path):

    word_collection = {};

    training_sample = [];
    training_label = [];

    Not_Wanted_char = dict.fromkeys(map(ord, '!#$%&/=?»:.,;|-_<>0123456789'), None);
    
    #Tratamento do conjunto de treino
    """ O csv será executado duas vezes: 
            1ª para criação do word_collection
            2ª para a criação do conjunto de treino já tratado """

    """ No futuro:
            * Pensar numa melhor forma de fazer a word_collection [Feito]
            * Nas samples é necessário a existencia de dar o numero de aparecição de cada palavra?"""
    
    # Criar o dicionário de palavras.
    with open(path, "r") as file:
        csvreader = csv.reader(file);
        for row in csvreader:
            string = row[1].lower() #Colocar as palavras em lowercase
            string = string.translate(Not_Wanted_char)     
            string = string.split(" ") #Transformar texto em lista

            for word in string:
                try:
                    word_collection[word]
                except KeyError:
                    word_collection[word] = word


    # Criar os training samples and label
    with open(path, "r") as file:
        csvreader = csv.reader(file);
        for row in csvreader:
            sample = []
            string = row[1].lower() #Colocar as palavras em lowercase
            string = string.translate(Not_Wanted_char)     
            string = string.split(" ") #Transformar texto em lista
                
            training_label.append(1 if row[0] == 'ham' else 0)
            for word in word_collection:
                if word in string:
                    sample.append(1);
                else:
                    sample.append(0);
                
                    
            training_sample.append(sample)

    return training_sample, training_label, word_collection

def evaluation_data_treatment(path, word_collection):

    training_sample = [];
    training_label = [];

    Not_Wanted_char = dict.fromkeys(map(ord, '!#$%&/=?»:.,;|-_<>0123456789'), None);

    with open(path, "r") as file:
        csvreader = csv.reader(file);
        for row in csvreader:
            sample = []
            string = row[1].lower() #Colocar as palavras em lowercase
            string = string.translate(Not_Wanted_char)     
            string = string.split(" ") #Transformar texto em lista
                
            training_label.append(1 if row[0] == 'ham' else 0)
            for word in word_collection:
                if word in string:
                    sample.append(1);
                else:
                    sample.append(0);
            
            training_sample.append(sample)

    return training_sample, training_label;


if __name__ == "__main__":

    p = Perceptron(learning_rate=0.1, n_iters=10);

    training_sample, training_label, word_collection = training_data_treatment("./././data/training.csv");

    # no fit vai ter de se dar input a uma array com os vetores das frases([0,1,1,0,1...]) e as labels que será uma array binária.
    p.fit(np.array(training_sample), np.array(training_label)) #Comando de aprendizagem da máquina

    training_sample_teste, training_label_teste = evaluation_data_treatment("./././data/test.csv", word_collection);

    prediction = p.predict(np.array(training_sample_teste))
    
    printMetrics(getMetrics(training_label_teste, prediction))
    
    training_data_validation, training_label_validation = evaluation_data_treatment("./././data/validation.csv", word_collection);

    prediction_val = p.predict(np.array(training_data_validation))

    printMetrics(getMetrics(training_label_validation, prediction_val))

    #print("Accuracy é: ", result)

    elapsed_time = timer() - start

    print("\n O tempo percorrido pelo programa é: ", elapsed_time, " segundos")