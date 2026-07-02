from Bio import Entrez
from Bio import SeqIO
import requests
disease_name = input("Enter the disease name :").lower().split()
corrected_name = " ".join(disease_name)
Entrez.email = "bhaswatimishra154@gmail.com"
try :
   handle = Entrez.esearch(
      db = "MedGen",
      term = f"{corrected_name}[exacttitle]"
    )
   record = Entrez.read(handle)
   print(record["IdList"])
   disease_id = record["IdList"]
   if len(disease_id) == 0 :
      handle = Entrez.esearch(
      db = "MedGen",
      term = f"{corrected_name}"
      )
      record = Entrez.read(handle)
      print(record["IdList"])
      new_disease_id = record["IdList"]
      print("Did you mean any of the diseases :")
      for new_disease_id in record["IdList"] :
        disease_data = Entrez.esummary(
        db = "MedGen",
        id = f"{new_disease_id}",
        retmode = "xml"
        )
        rec = Entrez.read(disease_data)
        print(rec["DocumentSummarySet"]["DocumentSummary"][0]["Title"])
   else :
     for disease_id in record["IdList"] :
        disease_data = Entrez.esummary(
        db = "MedGen",
        id = f"{disease_id}",
        retmode = "xml"
        )
        rec = Entrez.read(disease_data)
        title = rec["DocumentSummarySet"]["DocumentSummary"][0]["Title"]
        print(f"Title : {rec["DocumentSummarySet"]["DocumentSummary"][0]["Title"]}")
        print(f"Definition : {rec["DocumentSummarySet"]["DocumentSummary"][0]["Definition"]}")
        clinvar_data = Entrez.esearch(
              db = "ClinVar",
              term = f"{title}",
           )
        clinvar_record =Entrez.read(clinvar_data)

        clinvar_id = clinvar_record["IdList"]
        mutation= {}
        for i, clinvar_id in enumerate(clinvar_record["IdList"],start = 1):
             clinvar_summary = Entrez.esummary(
                 db = "ClinVar",
                 id = f"{clinvar_id}",
                 retmode = "xml"
              )
             clinvar_rec = Entrez.read(clinvar_summary, validate = False)
             print(i)
             print(f"variant type : {clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["obj_type"]}")
             print(f" Gene name : {clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["gene_sort"]}")
             print(f" Chromosome no. : {clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["chr_sort"]}")
             print(f"protein change : {clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["protein_change"]}")
             print(f" Gene id : {clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["genes"][0]["GeneID"]}")
             gene = clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["gene_sort"]
             mutation[gene] = []
             protein = clinvar_rec["DocumentSummarySet"]["DocumentSummary"][0]["protein_change"]
             mutation[gene].append(protein)

except Exception as E :
   print( f"error : {E}")
gene_name = input("Enter the gene name :").upper()
for gene in mutation.keys() :
   if gene_name == gene :
      print(mutation[gene])
def protein_info(gene_name,mutation) :
   try :
      organism = input("Enter the name of organism :").split()
      corrected_organism = " ".join(organism)
      url = (f"https://rest.uniprot.org/uniprotkb/search?query=gene_exact:{gene_name}+AND+organism_name:{corrected_organism}+AND+reviewed:true&format=json")
      protein_info = requests.get(url)
      data = protein_info.json()
      print(data["results"][0]["primaryAccession"])
      uniport_id = data["results"][0]["primaryAccession"]
      fasta_url = (f"https://rest.uniprot.org/uniprotkb/{uniport_id}.fasta")
      response = requests.get(fasta_url).text
      with open("disease_protein.fasta","w") as f :
         f.write(response)
      parser = SeqIO.parse("disease_protein.fasta","fasta")
      parser_list = list(parser)
      sequence = parser_list[0].seq
      for protein in mutation[gene_name] :
         if "fs" in protein :
            print (f"frameshift mutation detected. Please check the fasta file for the original protein sequence.")
         elif "*" in protein :
            print(f"nonsense mutation detected. Please check the fasta file for the original protein sequence.")
            header= f">Nonsence_mutaion_seq{protein}"
            cut_position = int(protein[1:-1])
            new_sequence = sequence[:cut_position-1] + "*"
            with open("disease_protein.fasta","a") as f :
               f.write(header)
               f.write("\n")
               f.write(new_sequence)
         else :
            cut_position = int(protein[1:-1])
            new_aa = protein[-1]
            header = f">missence_mutation_seq{protein}"
            if sequence[cut_position-1] == protein[0] :
               new_sequence = sequence[:cut_position-1] + new_aa + sequence[cut_position:]
               with open("disease_protein.fasta","a") as f :
                  f.write(header)
                  f.write("\n")
                  f.write(new_sequence)
   except Exception as E :
      print(f"error : {E}")
protein_info(gene_name,mutation)
