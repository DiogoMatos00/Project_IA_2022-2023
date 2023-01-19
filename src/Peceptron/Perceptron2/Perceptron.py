import csv;
import math;


#Tratamento do conjuntos de dados
def data_treatment(path):

    data = list();

    #Caracteres não desejados
    Not_Wanted_char = dict.fromkeys(map(ord, '!#$%&/=?»:.,;|-_<>0123456789'), None);

 
    with open(path, "r") as file:
        csvreader = csv.reader(file);
        for row in csvreader:
            mail = dict();
            words = dict();

            # Transformar o ham e o spam em 1 e -1 respetivamente.
            if row[0] == "ham":
                mail['label'] = 1;
            else:
                mail['label'] = -1

            #Tratamento da informação
            string = row[1].lower() #Colocar as palavras em lowercase
            string = string.translate(Not_Wanted_char)     
            string = string.split(" ") #Transformar texto em lista

            #Criar a coleção de palavras em cada mail
            for word in string:
                try:
                    words[word] = words[word] +1
                except KeyError:
                    words[word] = 2

            mail['words'] = words;

            data.append(mail);

    #Ex: ['label': 1, 'words': {'have': 2, 'you': 2, 'heard': 2, 'from': 2, 'this': 2, 'week': 2}]
    return data;

def perceptron(train_data, T):
    #Cria o dicionário teta. (Todas as palavras com valor 0)
    teta = dict();
    for mail in train_data:
         for word, count in mail['words'].items():
            if word not in teta:
                try:
                    teta[word]
                except KeyError:
                    teta[word] = 0

    teta_zero = 0
    for _ in range(T):
        for mail in train_data:
            #A linha abaixo é a linha 5 do pseudo-código que o professor tem no e-learning.
            if mail['label'] * classify(teta, mail['words'], teta_zero) <= 0:
                for word, count in mail['words'].items():
                    if word in teta:
                        teta[word] += mail['label'] * count
                teta_zero += mail['label']

    return teta, teta_zero


# Classifica se um mail é spam ou ham.
def classify(teta, mail, teta_zero):
    total_sum = 0
    for word, count in mail.items():
        if word in teta:
            total_sum += teta[word] * count
    return total_sum + teta_zero

def data_analysis(data, teta, teta_zero):
    Metrics = {
        'tp': 0,
        'fp': 0,
        'tn': 0,
        'fn': 0,
    }

    for mail in data:
        #Dado um email, vai classificar se é spam ou ham.
        #Math.copysign apenas retorna -1 ou 1 com base no sinal da segunda
        #variavel na função. (Ex. -43 dá -1, e 561 dá 1)
        classifier = classify(teta, mail['words'], teta_zero)
        if classifier > 0:
            if mail['label'] > 0:
                Metrics['tp'] += 1
            else:
                Metrics['fp'] += 1
        else:
            if mail['label'] < 0:
                Metrics['tn'] += 1
            else:
                Metrics['fn'] += 1

    return Metrics

def getMetrics(data: dict):
    Metrics = {
        'tp': data['tp'],
        'fp': data['tn'],
        'tn': data['fp'],
        'fn': data['fn'],
        'acc': 0,
        'err': 0,
        'sn': 0,
        'sp': 0,
        'p': 0,
        'r': 0,
        'fm': 0,
        'gm': 0
    }

    tp = data['tp'];
    tn = data['tn'];
    fp = data['fp'];
    fn = data['fn'];

    Metrics['acc'] = (tp + tn)/(tp + tn + fp + fn);
    Metrics['err'] = (fp + fn)/(tp + tn + fp + fn);
    Metrics['sn'] = tp/(tp+fn);
    Metrics['sp'] = tn/(tn+fp);
    Metrics['p'] = tp/(tp+fp);
    Metrics['r'] = tp/(tp+tn);
    Metrics['fm'] = (2 * Metrics['p'] * Metrics['r'])/(Metrics['p'] + Metrics['r']);
    Metrics['gm'] = math.sqrt(tp * tn) ;

    return Metrics;

def printMetrics(data: dict, data_type):
    print("""

        Métricas e matriz de erro para o {} com Percetrão:

        =====================================================
        Matriz de Erro:

                                    Valor Predito
                        ____Positive_________Negative____
        Valor           |               |               |
        Real   Postive  | TP = {}      | FN = {}        |   
                        |_______________|_______________|
                        |               |               |
               Negative | FP = {}      | TN = {}        |
                        |_______________|_______________|



        =====================================================
        Métricas:
        Accuracy(acc) : {}
        Error Rate(err) : {}
        Sensitivity(sn) : {}
        Specificity(sp) : {}
        Precision(p) : {}
        Recall(r) : {}
        F-Measure(FM) : {}
        Geometric-mean(GM) : {}

    """.format(data_type, data['tp'], data['fn'], data['fp'], data['tn'], data['acc'], data['err'], data['sn'], data['sp'], data['p'], data['r'], data['fm'], data['gm']))


if __name__ == "__main__":

    training_data = data_treatment("./././data/training.csv")
    teta, tetazero = perceptron(training_data, 100)

    validation_data = data_treatment("./././data/test.csv")
    Result = data_analysis(validation_data, teta, tetazero)
    printMetrics(getMetrics(Result), "Conjunto de teste")

    validation_data = data_treatment("./././data/validation.csv")
    Result = data_analysis(validation_data, teta, tetazero)
    printMetrics(getMetrics(Result), "Conjunto de validação")