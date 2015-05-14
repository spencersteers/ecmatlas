import sys
import csv
import re
import io

EXPERIMENT_HEADER_END_STRING = '***Per experiment values***'
EXPERIMENT_END_STRING = '***Per sample values***'
CONCENTRATIONS_END_STRING = 'PeptideSequence'
EXPERIMENT_FIELDS_PATTERN_STR = '({0}[:|,])([^,]+)'
METADATA_CONCENTRATION_SPLIT_PATTERN = re.compile(r'(Gene,.*\n)')


EXPERIMENT_FIELDS = [('Experiment', 'name'), ('Species', 'species'), ('Data Type', 'data_type'), ('Acquisition Instrument','acquisition_instrument'),
                     ('Acquisition Type', 'acquisition_instrument'), ('Run Time', 'run_time'), ('Publication URL', 'publication'),
                     ('Data Depository Link', 'data_depository_link')]

def parse_dataset(file_path):
    # print 'start'
    f = open(file_path, 'r')
    f_str = f.read()

    # grab all text up intil experiment delimeter
    first_split = f_str.split(EXPERIMENT_END_STRING)
    experiment_csv = first_split[0]

    # remove remaining columns/commas after delimiter (***Per experiment values***)
    second_split = first_split[1].split('\n', maxsplit=1)
    remaining_string = second_split[1]

    # split remaining string into concentrations and tissue weight norm sections
    third_split = remaining_string.split(CONCENTRATIONS_END_STRING)
    concentrations_csv = third_split[0]
    dataset_items_csv = CONCENTRATIONS_END_STRING + third_split[1]

    experiment = parse_experiment(experiment_csv)
    dataset_items = parse_dataset_items(dataset_items_csv)
    concentrations = parse_concentrations(concentrations_csv)

    return {'experiment': experiment, 'dataset_items': dataset_items, 'concentrations': concentrations}


def split_to_sections(dataset_file_name):
    with open (dataset_file_name) as dataset_file:
        dataset_str = dataset_file.read()
        EXPERIMENT_END_PATTERN.search(dataset_str)


def parse_experiment(csv_experiment):

    experiment = dict()
    for field, model_field in EXPERIMENT_FIELDS:
        result = re.search(EXPERIMENT_FIELDS_PATTERN_STR.format(field), csv_experiment, re.M)
        experiment[model_field] = result.group(2)

    return experiment

def parse_concentrations(csv_relative_concentrations):

    metadata_csv, concentrations_csv = split_metadata_concentrations(csv_relative_concentrations)

    # break metadata csv into indexed columns for easy use
    # [Sex, Disease State, Disease Note, Age, Sample identifier, Time point, Fraction, Tissue]
    per_sample_metadata = list()
    for col in zip(*csv.reader(io.StringIO(metadata_csv), delimiter=',')):
        per_sample_metadata.append(col)

    # now iterate through actual values
    # at each index in a row combine gene (row[0])
    # with concentration value (per_sameple_data[index]  when index > 0)
    index = 0
    concentrations = list()
    for row in csv.reader(io.StringIO(concentrations_csv), delimiter=','):

        # skip lines with just commas
        if not row[0]:
            continue
        # set gene name
        gene = row[0]

        # skip gene name
        enumerated_rows = enumerate(row)
        next(enumerated_rows, None)

        for index, value in enumerated_rows:
            # copy sample meta data and append gene/value
            # [Sex, Disease State, Disease Note, Age, Sample identifier, Time point, Fraction, Tissue, ConcentrationValue, Gene]
            concentration_item = list(per_sample_metadata[index])
            concentration_item.append(value)
            concentration_item.append(gene)
            concentrations.append(concentration_item_to_dict(concentration_item))

    return concentrations


def split_metadata_concentrations(csv_relative_concentrations):

    # split sample meta data and concentration/gene/tissue values
    metadata_concentrations_split = METADATA_CONCENTRATION_SPLIT_PATTERN.split(csv_relative_concentrations)

    # the split leaves us with 3 groups: [sample metadata before gene header row],  [gene header row], [concentration values]
    # join [metadata] and [gene header] together
    metadata_csv = metadata_concentrations_split[0] + metadata_concentrations_split[1]
    concentrations_csv = metadata_concentrations_split[2]

    return metadata_csv, concentrations_csv


def concentration_item_to_dict(row):
    return {
        'sex': row[0].strip(),
        'disease_state': row[1].strip(),
        'disease_note': row[2].strip(),
        'age': row[3].strip(),
        'sample_identifier': row[4].strip(),
        'time_point': row[5].strip(),
        'fraction': row[6].strip(),
        'tissue': row[7].strip(),
        'value': row[8].strip(),
        'gene': row[9].strip(),
    }


def parse_dataset_items(dataset_items_csv):
    dataset_items = []

    csv_reader = csv.reader(io.StringIO(dataset_items_csv), delimiter=',')
    next(csv_reader, None)  # skip header
    for row in csv_reader:
        # dataset_items.append(dataset_item_to_dict(row))
    
        row_tissue1 = row
        row_tissue1[9] = "Skin"
        row_tissue1[10] = row[11]
        dataset_items.append(dataset_item_to_dict(row_tissue1))

        row_tissue2 = row
        row_tissue2[9] = "Bone"
        row_tissue2[10] = row[12]
        dataset_items.append(dataset_item_to_dict(row_tissue2))

        row_tissue3 = row
        row_tissue3[9] = "Muscle"
        row_tissue3[10] = row[13]
        dataset_items.append(dataset_item_to_dict(row_tissue3))

        row_tissue4 = row
        row_tissue4[9] = "Tendon"
        row_tissue4[10] = row[14]
        dataset_items.append(dataset_item_to_dict(row_tissue4))

    return dataset_items

def dataset_item_to_dict(row):
    return {
        'sequence': row[0].strip(),
        'gene_name': row[1].strip(),
        'molecular_weight': row[2].strip(),
        'protein_name': row[3].strip(),
        'functional_group_name': row[4].strip(),
        'family_name': row[5].strip(),
        'species_name': row[6].strip(),
        'tissue_name': row[9].strip(),
        'tissue_weight_norm': row[10].strip()
    }

if __name__ == '__main__':
    main()