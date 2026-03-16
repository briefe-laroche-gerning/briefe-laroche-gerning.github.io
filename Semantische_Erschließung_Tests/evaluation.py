# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Funktionen zur Visualisierung der Ergebnisse der Schlagwort-Annotation mit LLMs (Percision, Recall, F1) #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

letter_numbers = list(range(1, 26))

# True Positives: Relevante, vom Modell annotierte Schlagworte:
tp = [0, 2, 4, 4, 2, 1, 3, 5, 2, 1, 2, 2, 1, 3, 4, 5, 3, 2, 3, 5, 1, 2, 1, 2, 1]
# True Positives, aber es zählen auch Oberbegriffe und leichte Abwandlungen der Begriffe als korrekt
tp_relaxed = [1, 2, 4, 4, 3, 3, 4, 5, 3, 2, 2, 2, 1, 5, 4, 5, 4, 2, 3, 6, 1, 2, 2, 5, 3]

# Vom Modell annotierte Schlagworte:
annotated = [10, 12, 10, 10, 10, 14, 10, 12, 13, 10, 8, 10, 10, 10, 11, 9, 10, 10, 8, 10, 10, 11, 10, 10, 7]
# Relevante Schlagworte (manuell annotiert):
relevant = [4, 9, 7, 6, 5, 7, 4, 9, 4, 4, 6, 3, 6, 7, 8, 15, 9, 6, 7, 11, 7, 8, 6, 8, 4]
# Durchschnitt: 170/25 = 6,8 = ca. 7


def list_division(numerator: List[float], denominator: List[float]):
    """
    Führt Division zweier Listen durch, wobei jeweils die Zahl an Stelle i der ersten Liste
    durch die Zahl an Stelle i der zweiten Liste dividiert wird.
    Returns: List[float]
    """

    result = []

    for i, (num, den) in enumerate(zip(numerator, denominator)):
        if den == 0:
            raise ZeroDivisionError(f"Division durch 0 an Index {i}.")
        result.append(num / den)

    return result


def f1_score(precision: List[float], recall: List[float]) -> List[float]:
    """
    Berechnet das F1-Maß zweier Listen.
    """
    result = []

    for i, (prec, rec) in enumerate(zip(precision, recall)):
        if (prec+rec) == 0.0:
            result.append(0.0)

        else:
            result.append((2.0*prec*rec) / (prec+rec))

    return result


def visualize(precision_list, precision_relaxed_list, recall_list, recall_relaxed_list, f1_list, f1_relaxed_list):
    """
    Visualisiert die Precision, Recall und F1-Werte mithilfe von Seaborn.
    """

    df_precision = pd.DataFrame({
    "Briefnummer": letter_numbers * 2,
    "Precision": precision_list + precision_relaxed_list,
    "Schlagwortabgleich": ["Exakt"] * 25 + ["Erweitert"] * 25
    })

    df_recall = pd.DataFrame({
    "Briefnummer": letter_numbers * 2,
    "Recall": recall_list + recall_relaxed_list,
    "Schlagwortabgleich": ["Exakt"] * 25 + ["Erweitert"] * 25
    })

    df_f1 = pd.DataFrame({
    "Briefnummer": letter_numbers * 2,
    "F1-Maß": f1_list + f1_relaxed_list,
    "Schlagwortabgleich": ["Exakt"] * 25 + ["Erweitert"] * 25
    })

    precision_plot = sns.barplot(
    data=df_precision,
    x="Briefnummer",
    y="Precision",
    hue="Schlagwortabgleich",
    width=0.65
    )
    precision_plot.legend(title="Schlagwortabgleich", loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=2)
    plt.savefig(
    "./data/output/LLM_evaluation_charts/precision_barchart.png",
    dpi=300,
    bbox_inches="tight",
    transparent=False)
    plt.close()
    
    recall_plot = sns.barplot(
    data=df_recall,
    x="Briefnummer",
    y="Recall",
    hue="Schlagwortabgleich",
    width=0.65
    )
    recall_plot.legend(title="Schlagwortabgleich", loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=2)
    plt.savefig(
    "./data/output/LLM_evaluation_charts/recall_barchart.png",
    dpi=300,
    bbox_inches="tight",
    transparent=False)
    plt.close()

    f1_plot = sns.barplot(
    data=df_f1,
    x="Briefnummer",
    y="F1-Maß",
    hue="Schlagwortabgleich",
    width=0.65
    )
    f1_plot.legend(title="Schlagwortabgleich", loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=2)
    plt.savefig(
    "./data/output/LLM_evaluation_charts/f1_barchart.png",
    dpi=300,
    bbox_inches="tight",
    transparent=False)
    plt.close()


def main():
    print("precision")
    precision = list_division(tp, annotated)
    print(precision)
    print("mean:")
    print(np.mean(precision))

    print("recall")
    recall = list_division(tp, relevant)
    print(recall)
    print("mean:")
    print(np.mean(recall))

    f1 = f1_score(precision, recall)
    print("F1-Score:")
    print(f1)
    print("mean:")
    print(np.mean(f1))

    print("Relaxed rules means")
    precision_relaxed = list_division(tp_relaxed, annotated)
    recall_relaxed = list_division(tp_relaxed, relevant)
    f1_relaxed = f1_score(precision_relaxed, recall_relaxed)
    print("Precision: ", np.mean(precision_relaxed), "Recall: ", np.mean(recall_relaxed), "F1: ", np.mean(f1_relaxed))

    visualize(precision_list=precision, precision_relaxed_list=precision_relaxed, recall_list=recall, recall_relaxed_list=recall_relaxed,
              f1_list=f1, f1_relaxed_list=f1_relaxed)


main()