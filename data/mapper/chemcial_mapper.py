if __name__ == '__main__':
    import pandas as pd
    import os
    import json
    from collections import defaultdict
    from tqdm import tqdm
    from pemt.utils import get_chemical_names

    analysis_name = 'ad'

    # Add caching system
    cache_dict = {}
    cache = 0
    genes_skipped = 0

    if os.path.exists(f"{analysis_name}_chemical_names.json"):
        chemical_names = json.load(
            open(f"{analysis_name}_chemical_names.json")
        )
    else:
        chemical_names = defaultdict(str)

    if os.path.exists(f"{analysis_name}_gene_to_chemicals.json"):
        gene_chemical_dict = json.load(
            open(f"{analysis_name}_gene_to_chemicals.json")
        )
    else:
        raise FileNotFoundError(
            f"Please ensure that you run the experimental data extractor file first."
        )

    for genes in tqdm(
        gene_chemical_dict, desc="Harmonizing chemicals for patent retrieval"
    ):
        # Extract chemical-target data from ChEMBL
        chemical_list = gene_chemical_dict[genes]

        if len(chemical_list) < 1:
            genes_skipped += 1
            continue

        for chembl_id in chemical_list:
            # Get name for chemical and store in dict
            if chembl_id not in chemical_names:
                cache += 1
                chemical_names[chembl_id] = get_chemical_names(chembl_id)

            if cache == 10:
                # Save chemical mapping dict for re-use
                with open(
                    f"{analysis_name}_chemical_names.json", "w"
                ) as f:
                    json.dump(chemical_names, f, ensure_ascii=False, indent=2)

                cache = 0