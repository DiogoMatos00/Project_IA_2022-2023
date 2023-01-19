import csv;
import math;

# Coleção de grupo de controlo
Ham_Collection = {'Probability_of_Ham': 0.5,'tota_num_words': 0}; # Dicionário com Ham tratado
Spam_Collection = {'Probability_of_Spam': 0.5,'tota_num_words': 0}; # Dicionário com Spam tratado
n_Ham = 0;
n_Spam = 0;


# Caractéres que não queremos dentro das frases. (Limpeza de dados)
# Python 3 utiliza strings com Unicode.
Not_Wanted_char = dict.fromkeys(map(ord, '!#$%&/=?»:.,;|-_<>0123456789'), None);

# Tratar do conjunto de dados de controlo (Spam ou Ham)
def data_treatment(path: str, debug: bool = 0):
    with open(path, "r") as file:
        global n_Ham;
        global n_Spam;
        csvreader = csv.reader(file);
        for row in csvreader:
            if(row[0] == "ham"):
                n_Ham += 1;                                                                          #Nº de frases Ham
                row[1] = row[1].lower();
                text = row[1].split();
                for i in text:
                    i = i.translate(Not_Wanted_char)                                                 #Tratamento do texto
                    if(i in Ham_Collection):
                        Ham_Collection[i] = Ham_Collection[i] + 1;
                    else:
                        Ham_Collection[i] = 2;                                                       # 2 porque é 1 pelo o primeiro e mais 1 pela existencia de palavras não defenidas  
                    Ham_Collection['tota_num_words'] = Ham_Collection['tota_num_words'] + 1
            elif(row[0] == "spam"):
                n_Spam += 1;                                                                         #Nº de frases Spam
                row[1] = row[1].lower();
                text = row[1].split();
                for i in text:
                    i = i.translate(Not_Wanted_char)
                    if(i in Spam_Collection):
                        Spam_Collection[i] = Spam_Collection[i] + 1;
                    else:
                        Spam_Collection[i] = 2;
                    Spam_Collection['tota_num_words'] = Spam_Collection['tota_num_words'] + 1     # 2 porque é 1 pelo o primeiro e mais 1 pela existencia de palavras não defenidas

    if(debug == 1):
        #Debug ver dicionário :)
        print("Ham Dictionary:\n")
        for key, value in Ham_Collection.items():
            print(key, ' : ', value)

        print("\n\n\n\n")

        print("Spam Dictionary:\n")
        for key, value in Spam_Collection.items():
            print(key, ' : ', value)

        print("\n\n\n\n")

    
    setProbability()

    print("Successfully processed data.");
    return;

def setProbability():
    Ham_Collection['Probability_of_Ham'] = n_Ham/(n_Ham+n_Spam);
    Spam_Collection['Probability_of_Spam'] = n_Spam/(n_Ham+n_Spam);

def data_analyse(path: str):
    Metrics = {
        'tp': 0,
        'fp': 0,
        'tn': 0,
        'fn': 0,
    }
    
    n_total = 0
    with open(path, "r") as file:
        csvreader = csv.reader(file);
        for row in csvreader:
            type = 1
            n_total += 1
            row[1] = row[1].lower();
            text = row[1].split();
            ham = []
            none_existence_ham_words = 0
            ham_prob = Ham_Collection['Probability_of_Ham'];
            spam = []
            none_existence_spam_words = 0
            spam_prob = Spam_Collection['Probability_of_Spam'];

            for i in text:
                i = i.translate(Not_Wanted_char)

                if(i in Ham_Collection):
                    ham.append(Ham_Collection[i]);
                else:
                    none_existence_ham_words += 2;
                    ham.append(1);

                if(i in Spam_Collection):
                    spam.append(Spam_Collection[i]);
                else:
                    none_existence_spam_words += 2;
                    spam.append(1);

            for i in ham:
                ham_prob = ham_prob * (i/(Ham_Collection['tota_num_words'] + none_existence_ham_words))


            for i in spam:
                spam_prob = spam_prob * (i/(Spam_Collection['tota_num_words'] + none_existence_spam_words))

            if(ham_prob > spam_prob):
                type = "ham";
            else:
                type = "spam";

            if(type == "ham"):
                if(type == row[0]):
                    Metrics['tp'] += 1;
                else:
                    Metrics['fp'] += 1;

            else:
                if(type == row[0]):
                    Metrics['tn'] += 1;
                else:
                    Metrics['fn'] += 1;


    return Metrics;

def getMetrics(data: dict):
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

#Colocar numero de positivos e negativos
def printMetrics(data: dict):
    print("""

        Metrics for data processing with Naive Bayes
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

data_treatment("././data/training.csv")

#print(data_analyse("./Conjunto de dados/conjunto de treino.csv"))
printMetrics(getMetrics(data_analyse("././data/test.csv")))
printMetrics(getMetrics(data_analyse("././data/validation.csv")))
