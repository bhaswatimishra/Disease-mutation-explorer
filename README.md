

This project is a Python-based bioinformatics pipeline that integrates **NCBI MedGen**, **ClinVar**, and **UniProt** to retrieve disease information, identify disease-associated protein variants, and generate mutant protein sequences.

This project demonstrates how multiple biological databases can be connected into a single workflow using Biopython, Entrez, REST APIs, and sequence manipulation techniques.

---

## Features

- Search diseases using **NCBI MedGen**
- Exact disease search with fallback suggestion system
- Retrieve disease title and definition
- Identify disease-associated variants from **ClinVar**
- Display:
  - Variant type
  - Gene name
  - Chromosome
  - Protein change
  - Gene ID
- Retrieve reviewed protein sequences from **UniProt**
- Download protein sequence in FASTA format
- Generate mutant protein sequences for supported mutations
- Save both reference and mutant protein sequences in a FASTA file

---

## Workflow

```
Disease Name
      │
      ▼
NCBI MedGen
      │
      ▼
Disease Information
      │
      ▼
ClinVar
      │
      ▼
Disease-associated Variants
      │
      ▼
User selects Gene
      │
      ▼
UniProt
      │
      ▼
Reference Protein Sequence
      │
      ▼
Mutation Processing
      │
      ▼
Mutant Protein FASTA
```

---

## Databases Used

| Database | Purpose |
|----------|---------|
| MedGen | Disease search and disease information |
| ClinVar | Disease-associated variants |
| UniProt | Reviewed protein sequence retrieval |

---

## Mutation Support

| Mutation Type | Supported |
|--------------|-----------|
| Missense | ✅ |
| Nonsense | ✅ |
| Frameshift | Detection only |

---

## Example Output

```
Disease : Parkinson disease

Gene : PINK1
Protein Change : D430*

Gene : VPS35
Protein Change : M40I
```

Generated FASTA:

```
>Reference_Protein
MAAA...

>Missense_M40I
MAIA...

>Nonsense_D430*
MAAA...
*
```

---

## Limitations

- Currently supports simple protein mutation formats such as **R272Q** and **Q516***.
- Complex HGVS protein expressions (for example, **p.Gln1648Glu**) are not parsed automatically.
- Frameshift mutations are detected but mutant protein sequences are not generated because predicting the downstream translated protein requires reconstruction of the altered coding sequence.
- Protein retrieval depends on the availability of a reviewed UniProt entry.
- The generated mutant sequences are computationally modified reference sequences and should not be considered experimentally validated proteins.

---

## Technologies Used

- Python
- Biopython
- Requests
- NCBI Entrez API
- UniProt REST API

---

## Learning Objectives

This project demonstrates:

- Biological database integration
- Entrez programming with Biopython
- REST API usage
- FASTA parsing
- Protein sequence manipulation
- Mutation modelling
- Bioinformatics workflow development
---

