import csv
import sys

# Sequence Gene MW Protein Functional Family Species Tissue Note TissueWeightNorm
def row_to_dict(row):
    return {
        'sequence': row[0],
        'gene_name': row[1],
        'molecular_weight': row[2],
        'protein_name': row[3],
        'functional_group_name': row[4],
        'family_name': row[5],
        'species_name': row[6],
        'tissue_name': row[7],
        'tissue_weight_norm': row[9]
    }


def parse_to_items(csv_file_name):
    dataset_items = []

    with open(csv_file_name) as file_obj:
        csv_reader = csv.reader(file_obj)
        next(csv_reader, None)  # skip header
        for row in csv_reader:
            dataset_items.append(row_to_dict(row))

    return dataset_items
