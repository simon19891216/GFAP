#!/usr/bin/env python
# -*- coding:utf-8 -*-


import argparse
import re,os,subprocess,pickle,gzip,json,random,scipy,itertools
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF



def argparseFunc():
  parser = argparse.ArgumentParser(description="design sgRNA")
  #input and output
  parser.add_argument('-o',"--out",help="save path")
  parser.add_argument('-qn',"--query_cds",help="the pathway of coding-sequence file")
  parser.add_argument('-qp',"--query_protein",help="the pathway of protein-sequence file")
  #selecting the annotation method
  parser.add_argument('-aws',"--annotation_with_species",help="the default is Arabidopsis_thaliana(Brassicaceae)")
  parser.add_argument('-awd',"--annotation_with_database",help="need to input the database name: psd, td, nr or swissprot.\
    psd: plant-special database, td: total database, nr: Non-redundant protein sequence database. ")
  #annotation for protein or CDS
  parser.add_argument("-go",action="store_true",help="annotating genes with GO information")
  parser.add_argument("-kegg",action="store_true",help="annotating genes with KEGG information")
  parser.add_argument("-pfam",action="store_true",help="annotating genes with protein-domain information")
  parser.add_argument("-only_ID",help="In addition to the annotation results, GFAP will provide a file containing only IDs.")
  parser.add_argument('-e','--e_value',type=str, default='1e-5',help='the default value of e-value is 1e-5')
  parser.add_argument("-am","--alignment_model",help="fast or sensitive, the default is fast")
  parser.add_argument("-ap","--alignment_percent",type=float,help="the screening threshold value for alignment results. the default is 80")
  parser.add_argument("-cpu",default="16",help="the default is 16")
  #annotation for ncRNA
  parser.add_argument("-nt","--ncRNA_type",help="for miRNA or lncRNA")
  parser.add_argument("-na","--ncRNA_annotation",action="store_true",help="for miRNA or lncRNA")
  #annotation with the information of a single gene family
  parser.add_argument("-sf","--single_family",action="store_true",help="identify the members of the interested family")
  parser.add_argument("-mn","--model_name",help="the model name of your interested family in GFAP database")#需要加一个参数以便用户可以查看有哪些收录的model
  parser.add_argument("-mp","--model_pathway",help="the pathway of the interested HMM model, if the model was not included into the GFAP family")
  #annotation with the information of multiplies gene families
  parser.add_argument("-mf","--multi_families",action="store_true",help="annotating genes with the informaiton of multi-families")
  parser.add_argument("-atf","--all_transcription_factor",action="store_true",help="annotating genes with the informaiton of transcription factors")
  parser.add_argument("-agf","--all_gene_families",action="store_true",help="annotating genes with the informaiton of gene families")
  #expand functions
  parser.add_argument("-t","--translate",action="store_true",help="translate CDS to protein sequences")#store_true的作用在于添加该参数后返回true值,注意加这个参数返回的是False,
  parser.add_argument("-rd","--RNA2DNA",action="store_true",help="transform RNA to DNA sequences")
  parser.add_argument("-ex","--extract_infor",action="store_true",help="extract information from annotation results based on the input ID file")
  parser.add_argument("-ID",help="input the ID or the file containing IDs")
  parser.add_argument("-exfid",action="store_true",help="the GO/PFAM/KEGG ID or the file containing IDs")
  parser.add_argument("-exgid",action="store_true",help="the gene ID or the file containing IDs")
  parser.add_argument("-ar","--annotation_result",help="the pathway of annotation results")
  parser.add_argument("-gf","--genomic_result",help="the transcriptome or transcriptome-like result. the example file can be found in the example subfolder of GFAP")
  parser.add_argument("-cf",action="store_true",help="the conversion function")
  parser.add_argument("-gid",type=int,help="the column index of gene IDs")
  parser.add_argument("-fid",type=int,help="the column index of go/gff")
  parser.add_argument("-pvalue",type=int,help="the column index of the p-value")
  parser.add_argument("-mr","--merge_result",action="store_true",help="merge different annotation results into one file")
  parser.add_argument("-rp","--results_pathway",help="need to put annotation results into an empty folder")
  #query information
  parser.add_argument("-as","--all_species",action="store_true",help="will show the species contained in GFAP")
  parser.add_argument("-af","--all_families",action="store_true",help="will show all families contained in GFAP")
  #draw
  parser.add_argument("-ds","--draw_statistics",action="store_true",help="will draw statistical results of annotations")
  parser.add_argument("-cut_value",default=10,type=int,help="the default is 10")
  parser.add_argument("-gn","--gene_number",default=0,type=int,help="the default is 0")
  parser.add_argument("-colormodel",default="r2cy",help="the default is r2cy")
  parser.add_argument("-singlecolor",action="store_true",help="will draw annotation results with a color")
  parser.add_argument("-drawtypes",help="bar chart or heatmap")
  parser.add_argument("-color",help="the comma as separator")
  parser.add_argument("-st","--save_type",help="svg or pdf")
  parser.add_argument("-dn","--draw_network",action="store_true",help="will draw network")
  parser.add_argument("-gca","--go_category",help="biological_process, cellular_component, molecular function")


  

  return parser.parse_args()

def annotprocess(totalfile,speciesfile,blastfile,savefile,algnment_percent):
    with gzip.open(totalfile,"rt") as f:
        content=f.readline()
        allgoinfor=json.loads(content)
    with gzip.open(speciesfile,"rt") as f:
        content=f.readline()
        changeid=json.loads(content)
    with open(blastfile,encoding="utf-8") as f,open(savefile,"w") as f1:
        allfors=set()
        for line in f:
            linelist=line.split("\t")
            geneid=linelist[0];refid=linelist[1];percent=float(linelist[2])
            if percent>=algnment_percent and refid in changeid:
                allfor={geneid+"\t"+allgoinfor[goid] for goid in changeid[refid] if goid in allgoinfor}
                allfors=allfors|allfor
        [print(infor,file=f1) for infor in allfors]

def annotprocess2(totalfile,blastfile,savefile,algnment_percent):
    with gzip.open(totalfile,"rt") as f:
        content=f.readline()
        allgoinfor=json.loads(content)
    with open(blastfile,encoding="utf-8") as f,open(savefile,"w") as f1:
        allfors={}
        for line in f:
            linelist=line.split("\t")
            queryid=linelist[0];targetid=linelist[1];percent=float(linelist[2])
            if percent>=algnment_percent and queryid not in allfors and targetid in allgoinfor:
                allfors[queryid]=queryid+"\t"+allgoinfor[targetid]
        [f1.write(infor+"\n") for infor in allfors.values()]
    os.remove(blastfile)

def align_annotation(filepath,inputtype,annotype,refspecies,evalue,algnment_type,algnment_percent,save,cpu,only_ID=None):#设定保存的路径，保存的一些参数需要变动
    if os.path.isdir(save)==False:save=os.path.dirname(save)#要有protein-alignment文件夹
    refspecies2=refspecies.split("(")[0]
    file2="./protein-alignment/"+refspecies2+".dmnd"
    if inputtype=="protein":
        if algnment_type!="sensitive":
            args='./bin/diamond blastp --db '+ file2+' --threads ' +cpu+' -q ' + filepath+ " -e " + evalue + ' -o ' + save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)#需要bin文件夹
            result.wait()
        else:
            args="./bin/diamond blastp --db "+file2+' --threads ' +cpu+" -q "+filepath+ " -e " + evalue +" --outfmt 6 --very-sensitive -o "+save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)
            result.wait()
    elif inputtype=="CDS":
        if algnment_type!="sensitive":
            args='./bin/diamond blastx --db '+ file2+' --threads ' +cpu+' -q ' + filepath+ " -e " + evalue + ' -o ' + save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)
            result.wait()
        else:
            args="./bin/diamond blastx --db "+file2+' --threads ' +cpu+" -q "+filepath+ " -e " + evalue +" --outfmt 6 --very-sensitive -o "+save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)
            result.wait()
    if "GO" in annotype:
        goidfile="./go/goafter/go_database.txt.gz"#这些文件夹要有
        geneid2goid="./go/goafter/"+refspecies+".txt.gz"#数据库名字要变
        blastfile=save+"/GFAP-blastresult.txt"
        savefile=save+"/GFAP-"+refspecies+"-GO_annotate.txt"
        annotprocess(goidfile,geneid2goid,blastfile,savefile,algnment_percent)
        if only_ID!=None:
            with open(savefile,encoding="utf-8") as f,open(save+"/GFAP-"+refspecies+"-GOID.txt","w") as f1:
                [print(line.split()[0]+"\t"+line.split()[1],file=f1) for line in f]
    if "KEGG" in annotype:
        goidfile="./kegg/keggafter/KEGG_database.txt.gz"
        geneid2goid="./kegg/keggafter/"+refspecies+".txt.gz"
        blastfile=save+"/GFAP-blastresult.txt"
        savefile=save+"/GFAP-"+refspecies+"-kegg_annotate.txt"
        annotprocess(goidfile,geneid2goid,blastfile,savefile,algnment_percent)
        if only_ID!=None:
            with open(savefile,encoding="utf-8") as f,open(save+"/GFAP-"+refspecies+"-keggID.txt","w") as f1:
                [print(line.split()[0]+"\t"+line.split()[1],file=f1) for line in f]
        if only_ID!=None:
            with gzip.open("./kegg/keggafter/k2ko.txt.gz","rt") as f:
                content=f.readline()
                allgoinfor=json.loads(content)
            with open(savefile,encoding="utf-8") as f,open(save+"/GFAP-"+refspecies+"-koID.txt","w") as f1:
                [print(line.split()[0]+"\t"+allgoinfor[line.split()[1]],file=f1) for line in f]
    if "pfam" in annotype:
        goidfile="./pfam/pfamafter/Pfam_database.txt.gz"
        geneid2goid="./pfam/pfamafter/"+refspecies+".txt.gz"
        blastfile=save+"/GFAP-blastresult.txt"
        savefile=save+"/GFAP-"+refspecies+"-pfam_annotate.txt"
        annotprocess(goidfile,geneid2goid,blastfile,savefile,algnment_percent)

def plantannotate(filepath,evalue,savefile,seqtype,annotatype,databasetype,cpu,only_ID=None):
    if evalue=="":evalue="1e-5"
    if os.path.isdir(savefile)==False:savefile=os.path.dirname(savefile)
    if seqtype=="CDS" or seqtype=="protein":
        if seqtype=="CDS":
            argument="./bin/seqkit translate "+filepath+" -o "+filepath+"-protein.txt"
            result=subprocess.Popen(argument,shell=True)
            result.wait()
            filepath=filepath+"-protein.txt"
        if "pfam" in annotatype or "GO" in annotatype:
            if databasetype=="psd":
                databasepath="./database/ppfam.txt.gz"
                databasepath2="./database/ppfam.txt"
            elif databasetype=="td":
                databasepath="./database/apg.txt.gz"
                databasepath2="./database/apg.txt"
            if os.path.exists(databasepath2)==False:
                g_file = gzip.GzipFile(databasepath)
                f=open(databasepath2,'wb')
                f.writelines(g_file)
                f.close()
                g_file.close()
                os.remove(databasepath)
            args="./bin/hmmsearch --noali --tblout ./pfam-hmmresult.txt"+" --cpu "+cpu+" -E "+evalue+" "+databasepath2+" "+filepath
            result=subprocess.Popen(args,shell=True)#这里，pfam的结果文件"./pfam-hmmresult.txt"应该存放在本目录下，用完后删除即可
            result.wait()
            if "pfam" in annotatype:
                with open("./pfam-hmmresult.txt",encoding="utf-8") as f,open(savefile+"/pfam_database_result.txt","w") as f1:
                    [print(line.split()[0]+"\t"+line.split()[3]+"\t"+line.split()[2].replace("_"," "),file=f1) for line in f if "#" not in line]
            if "GO" in annotatype:
                gofs=set()
                with gzip.open("./go/goafter/pfam2go.txt.gz","rt") as f:
                    content=f.readline()
                    allpfamgo=json.loads(content)
                with gzip.open("./go/goafter/go_database.txt.gz","rt") as f:
                    content=f.readline()
                    allgof=json.loads(content)
                with open("./pfam-hmmresult.txt",encoding="utf-8") as f,open(savefile+"/GO_database_result.txt","w") as f1:
                    for line in f:
                        if "#" not in line:
                            linelist=line.split()
                            geneid=linelist[0];pfamid=linelist[3].split(".")[0]
                            if pfamid in allpfamgo:
                                goid=allpfamgo[pfamid]
                                gof={geneid+"\t"+allgof[go] for go in goid}
                                gofs=gofs|gof
                    [print(go,file=f1) for go in gofs]
                if only_ID!=None:
                    with open(savefile+"/GO_database_result.txt",encoding="utf-8") as f,open(savefile+"/GO_ID_result.txt","w") as f1:
                        [print(line.split("\t")[0]+"\t"+line.split("\t")[1],file=f1) for line in f]
            os.remove("./pfam-hmmresult.txt")
        if "KEGG" in annotatype:
            databasepath2="./database/akegg.txt"
            args="./bin/hmmsearch --noali --tblout ./kegg-hmmresult.txt"+" --cpu "+cpu+" -E "+evalue+" "+databasepath2+" "+filepath
            result=subprocess.Popen(args,shell=True)#这里，kegg的结果文件"./pfam-hmmresult.txt"应该存放在本目录下，用完后删除即可
            result.wait()
            with gzip.open("./kegg/keggfunc.txt.gz","rt") as f:
                content=f.readline()
                allkegg=json.loads(content)
            with open("./kegg-hmmresult.txt",encoding="utf-8") as f,open(savefile+"/kegg_database_result.txt","w") as f1:
                [print(line.split()[0]+"\t"+allkegg[line.split()[2]],file=f1) for line in f if "#" not in line and line.split()[2] in allkegg]
            if only_ID!=None:
                with open(savefile+"/kegg_database_result.txt",encoding="utf-8") as f,open(savefile+"/kegg_id_result.txt","w") as f1:
                    [print(line.split()[0]+"\t"+line.split()[1],file=f1) for line in f]
                with gzip.open("./kegg/keggafter/k2ko.txt.gz","rt") as f:
                    content=f.readline()
                    allgoinfor=json.loads(content)
                with open(savefile+"/kegg_database_result.txt",encoding="utf-8") as f,open(savefile+"/kegg_koid_result.txt","w") as f1:
                    [print(line.split()[0]+"\t"+allgoinfor[line.split()[1]],file=f1) for line in f]
            os.remove("./kegg-hmmresult.txt")

def nr_swissprot(filepath,inputtype,databasetype,evalue,algnment_type,cpu,algnment_percent,save):#设定保存的路径，保存的一些参数需要变动
    if os.path.isdir(save)==False:save=os.path.dirname(save)#要有protein-alignment文件夹
    file2="./database/"+databasetype+".dmnd"
    if inputtype=="protein":
        if algnment_type!="sensitive":
            args='./bin/diamond blastp --db '+ file2+' --top 1'+' --threads ' +cpu+ ' -q ' + filepath+ " -e " + evalue + ' -o ' + save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)#需要bin文件夹
            result.wait()
        else:
            args="./bin/diamond blastp --db "+file2+' --top 1'+' --threads '+cpu+" -q "+filepath+ " -e " + evalue +" --outfmt 6 --very-sensitive -o "+save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)
            result.wait()
    elif inputtype=="CDS":
        if algnment_type!="sensitive":
            args='./bin/diamond blastx --db '+ file2+' --top 1'+' --threads ' +cpu+ ' -q ' + filepath+ " -e " + evalue + ' -o ' + save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)
            result.wait()
        else:
            args="./bin/diamond blastx --db "+file2+' --top 1'+' --threads '+cpu+" -q "+filepath+ " -e " + evalue +" --outfmt 6 --very-sensitive -o "+save+"/GFAP-blastresult.txt"
            result=subprocess.Popen(args,shell=True)
            result.wait()
    if "nr" in databasetype:
        goidfile="./database/nr_annotation.txt.gz"#
        blastfile=save+"/GFAP-blastresult.txt"
        save=save+"/nr_result.txt"
        annotprocess2(goidfile,blastfile,save,algnment_percent)
    if "swissprot" in databasetype:
        goidfile="./database/swissprot_annotation.txt.gz"
        blastfile=save+"/GFAP-blastresult.txt"
        save=save+"/swissprotf_result.txt"
        annotprocess2(goidfile,blastfile,save,algnment_percent)

def reverse_complement(sequence):
    trantab = str.maketrans('ACGTagct\n', 'TGCATCGA\n')
    string = sequence.translate(trantab)
    reverse_complement = string[::-1]
    return reverse_complement

def identify_miRNA(filepath,savefile,evalue,cpu,ncRNAtype):
    if ncRNAtype=="miRNA":
        file1="./database/miRNA_HMM.txt.gz"
        file2="./database/miRNA_HMM.txt"
    elif ncRNAtype=="lncRNA":
        file1="./database/lncRNA_HMM.txt.gz"
        file2="./database/lncRNA_HMM.txt"
    hmmfile=""
    with open(filepath,encoding="utf-8") as f:
            dirseq={}
            for line in f:
                if ">" in line:
                    ID=line.split()[0]+"_r"
                    dirseq[ID]=""
                else:
                    dirseq[ID]+=line.strip().upper()
    with open(filepath,"a") as f1:
        [f1.write("\n"+ID+"\n"+reverse_complement(seqs)) for ID,seqs in dirseq.items()]
    if os.path.exists(file2)==False:
        g_file = gzip.GzipFile(file1)
        f=open(file2,'wb')
        f.writelines(g_file)
        f.close()
        g_file.close()
        os.remove(file1)
    if os.path.isdir(savefile):
        args="./bin/hmmsearch --noali --tblout "+savefile+"/ncRNA_hmmresult.txt"+" --cpu "+cpu+" -E "+evalue+" "+file2+" "+filepath
        result=subprocess.Popen(args,shell=True)
        result.wait()
        hmmfile=savefile+"/ncRNA_hmmresult.txt"
        savefile=savefile+"/GFAP_miRNA_annotresult.txt"
    else:
        args="./bin/hmmsearch --noali --tblout "+savefile+"_ncRNA_hmmresult.txt"+" --cpu "+cpu+" -E "+evalue+" "+file2+" "+filepath
        result=subprocess.Popen(args,shell=True)
        hmmfile=savefile+"_ncRNA_hmmresult.txt"
        result.wait()
    with open(filepath,encoding="utf-8") as f:
        orignID={line.strip()[1:].replace("_r","") for line in f if ">" in line}
    with open(hmmfile,encoding="utf-8") as f:
        targetdir={}
        for line in f:
            if "#" not in line:
                linelist=line.split()
                geneid=linelist[0].replace("_r","");queryID=linelist[2];evalue=linelist[4]
                infor=queryID+"\t"+evalue
                if geneid not in targetdir:targetdir[geneid]=[infor]
                else:targetdir[geneid].append(infor)
    with open(savefile,"w") as f:
        f.write("gene_name\tncRNA_name\n")
        for i,j in targetdir.items():
            dirs={float(k.split("\t")[1]):k.split("\t")[0] for k in j}
            min_value=min(dirs.keys())
            key=dirs[min_value]
            f.write(i+"\t"+key+"\n")
        [f.write(ID+"\tmay be a new ncRNA\n") for ID in orignID if ID.replace("_r","") not in targetdir]
    os.remove(hmmfile)

def hmmsearch(hmm,file,save,cpu,evalue):
    args="./bin/hmmsearch --noali --tblout "+save+" --cpu "+cpu+" -E "+evalue+" "+hmm+" "+file
    result=subprocess.Popen(args,shell=True)
    result.wait()

def singlehmm(file):
    with open(file,encoding="utf-8") as f:
        line={line.split()[0] for line in f if "#" not in line}
        lines = '\n'.join(line)
        return lines

def multihmm(file,count):
    with open(file,encoding="utf-8") as f:
        lists = {line.split()[0]+"\t"+ line.split()[2] for line in f if "#" not in line}
        tlists=[line.split()[0] for line in lists]
        result=[i for i in tlists if tlists.count(i)==count]
        lines="\n".join(result)
        return lines

def exseqs(file,save,lines):
    indexfile=file+".index"
    save=save+"_seqs.txt"
    geneids=(lines).split("\n")
    with open(indexfile,"rb") as f:
        indexs=pickle.load(f)
    with open(file,"rb") as f2,open(save,"w") as f1:
        for line in geneids:
            if "sequences" not in line and line!="":
                ID=line.strip()
                print(">"+ID,file=f1)
                ID=ID.encode()
                if ID in indexs:
                    f2.seek(indexs[ID])
                    count=0
                    for line in f2:
                        if line.startswith(">".encode()):
                            count+=1
                        else:
                            print(line.decode().strip(),file=f1)
                        if count==2:
                            break

def singlefamily(filepath,model,save,cpu,evalue,model2=""):#model2允许用户自己加入
    basenames="hmmfile.txt"
    if model!="":
        model=model.split(" ")[0]
        file1="./gene_family/"+model+".hmm.gz"
        hmmf="./gene_family/"+model+".hmm"
        if os.path.exists(file1):
            g_file = gzip.GzipFile(file1)
            f=open(hmmf,'wb')
            f.writelines(g_file)
            f.close()
            g_file.close()
            os.remove(file1)
    if model2!="":hmmf=model2
    savefile="./"+basenames
    hmmsearch(hmmf,filepath,savefile,cpu,evalue)
    with open(hmmf,encoding="utf-8") as f:
        lists=f.readlines()
    count=lists.count("HMMER3/f [3.1b2 | February 2015]\n")
    if count==1:
        lines=singlehmm(savefile)
    else:
        lines=multihmm(savefile,count)
    with open(save,"w") as f:f.write("The sequences of the following IDs contained {} model\n".format(model)+lines)
    os.remove(savefile)
    if os.path.isfile(filepath+".index")==False:
        with open(filepath,"rb") as f:
            indexs={}
            index=f.tell()
            line=f.readline()
            while line:
                if ">".encode() in line:
                    ID=line.split()[0][1:]
                    indexs[ID]=index
                index=f.tell()
                line=f.readline()
        with open(filepath+".index","wb") as f:
            pickle.dump(indexs,f)
    exseqs(filepath,save,lines)

def alldomains(file):
    with open(file,encoding="utf-8") as f:
        lists = {line.split()[0]+"\t"+line.split()[2].replace("_"," ") for line in f if "#" not in line}
        lines = "\n".join(lists)
        return lines

def multifamilies(filepath,save,cpu,evalue,model):
    if os.path.isdir(save):save=save+"/GFAP_GF_result.txt"
    filebasename="targetfile.txt";basenames="hmmfile.txt"
    savefile="./"+basenames
    file1="./gene_family/"+model+".hmm.gz"
    hmmf="./gene_family/"+model+".hmm"
    if os.path.exists(file1):
        g_file = gzip.GzipFile(file1)
        f=open(hmmf,'wb')
        f.writelines(g_file)
        f.close()
        g_file.close()
        os.remove(file1)
    hmmsearch(hmmf,filepath,savefile,cpu,evalue)
    lines=alldomains(savefile)
    with open(save,"w") as f:f.write("gene_ID\tmodel_name\n"+lines)
    os.remove(savefile)
    if filebasename in filepath:os.remove(filepath)

def translatDNA(file,save):
    if os.path.isdir(save):save=save+"/GFAP_DNA2protein.txt"
    args="./bin/seqkit translate "+file+" -o "+save
    result=subprocess.Popen(args,shell=True)
    result.wait()

def rna2dna(file,save):
    if os.path.isdir(save):save=save+"/GFAP_RNA2DNA.txt"
    with open(file,encoding="utf-8") as f,open(save,"w") as f1:
        [f1.write(line.upper().replace("U","T")) if ">" not in line else f1.write(line) for line in f]

def ext(file,save,ID,IDtype):
    if os.path.isfile(ID):
        with open(ID,encoding="utf-8") as f:
            IDs={line.strip()+"\t" for line in f}
        with open(file,encoding="utf-8") as f,open(save,"w") as f1:
            if IDtype=="gid":
                [f1.write(line) for line in f if line.split("\t")[0]+"\t" in IDs]
            elif IDtype=="fid":
                [f1.write(line) for line in f if line.split("\t")[1]+"\t" in IDs]
    else:
        with open(file,encoding="utf-8") as f,open(save,"w") as f1:
            [f1.write(line) for line in f if ID+"\t" in line]

def dealwithtranscriptome(file,save,geneid,goid,pvalue):
    goandfunc="./go/go_func.txt.gz"#注释文件
    keggfunc="./kegg/keggfunc.txt.gz"
    geneid=int(geneid);goid=int(goid);pvalue=int(pvalue)
    pgo = re.compile('GO:\d{7}')
    pkegg=re.compile('K\d{5}')
    with gzip.open(goandfunc,"rt") as f:
        content=f.readline()
        gofunc = json.loads(content)
    with gzip.open(keggfunc,"rt") as f:
        content=f.readline()
        keggfunc = json.loads(content)
    if os.path.isdir(save):save=save+"/GFAP_transcriptome.txt"
    with open(file,encoding="utf-8") as f,open(save,"w") as f1:
        for line in f:
            linelist=line.split("\t")
            if "E" not in linelist[pvalue-1] and "0" not in linelist[pvalue-1]:
                continue
            else:
                if "GO:" in linelist[goid-1]:
                    golist=pgo.findall(linelist[goid-1])
                    [f1.write(linelist[geneid-1]+"\t"+gofunc[go]+"\t"+linelist[pvalue-1]+"\n") for go in golist if go in gofunc]
                elif "K" in linelist[goid-1]:
                    golist=pkegg.findall(linelist[goid-1])
                    [f1.write(linelist[geneid-1]+"\t"+keggfunc[go]+"\t"+linelist[pvalue-1]+"\n") for go in golist if go in keggfunc]

def funccollect(file):
    ff={}
    with open(file,encoding="utf-8") as f:
        for line in f:
            linelist=line.split("\t")
            ID=linelist[0];goid=linelist[1]
            if ID not in ff:ff[ID]=[]
            ff[ID].append(goid)
    ft={i:";".join(j) for i,j in ff.items()}
    return ft

def mergef(file,save,pathway):
    gof={};keggf={};pfamf={};nrf={};swissprotf={}
    with open(file,encoding="utf-8") as f:
        ids={line.split()[0][1:] for line in f if ">" in line}
    filelist=os.listdir(pathway)
    for file in filelist:#强制性要求用户名字中必须含有关键词
        file=pathway+"/"+file
        if "GO" in file:gof=funccollect(file)
        if "kegg" in file:keggf=funccollect(file)
        if "pfam" in file:pfamf=funccollect(file)
        if "nr" in file:nrf=funccollect(file)
        if "swissprotf" in file:swissprotf=funccollect(file)
    with open(save,"w") as f:
        infor=""
        f.write("ID\tnr\tswissprot\tGO\tKEGG\tPfam\n")
        for ID in ids:
            infor=ID
            if ID in nrf:infor+="\t"+nrf[ID]
            else:infor+="\t/"
            if ID in swissprotf:infor+="\t"+swissprotf[ID]
            else:infor+="\t/"
            if ID in gof:infor+="\t"+gof[ID]
            else:infor+="\t/"
            if ID in keggf:infor+="\t"+keggf[ID]
            else:infor+="\t/"
            if ID in pfamf:infor+="\t"+pfamf[ID]
            else:infor+="\t/"
            f.write(infor+"\n")
            infor=""

def drawgo(file,cutvalue,color,gene_number,singlecolor=False):
    with open(file,encoding="utf-8") as f:
        biological_process={};cellular_component={};molecular_function={}
        alllist=[];numbermax=[];number=cutvalue
        for line in f:
            if "Sorry" not in line:
                linelist=line.strip().split("\t")
                func=linelist[2];categ=linelist[3]
                if categ=="biological_process":
                    if func not in biological_process:
                        biological_process[func]=1
                    else:
                        biological_process[func]+=1
                elif categ=="cellular_component":
                    if func not in cellular_component:
                        cellular_component[func]=1
                    else:
                        cellular_component[func]+=1
                elif categ=="molecular_function":
                    if func not in molecular_function:
                        molecular_function[func]=1
                    else:
                        molecular_function[func]+=1
    if biological_process!={}:
        biological_process = {k: v for k, v in sorted(biological_process.items(), key=lambda item: item[1], reverse=True)}
        bp=list(biological_process.items())[:number]
        numbermax.append(int(bp[0][1]))
        if gene_number!=0:
            bp2=[i for i in bp if int(i[1])>gene_number]
            alllist.append(bp2)
        alllist.append(bp)
    if cellular_component!={}:
        cellular_component = {k: v for k, v in sorted(cellular_component.items(), key=lambda item: item[1], reverse=True)}
        cc=list(cellular_component.items())[:number]
        numbermax.append(int(cc[0][1]))
        if gene_number!=0:
            cc2=[i for i in cc if int(i[1])>gene_number]
            alllist.append(cc2)
        alllist.append(cc)
    if molecular_function!={}:
        molecular_function = {k: v for k, v in sorted(molecular_function.items(), key=lambda item: item[1], reverse=True)}
        mf=list(molecular_function.items())[:number]
        numbermax.append(int(mf[0][1]))
        if gene_number!=0:
            mf2=[i for i in mf if int(i[1])>gene_number]
            alllist.append(mf2)
        alllist.append(mf)
    ql=max(numbermax);ymax=number*6+4
    if 100<ql*10**-6<1000:unit=10**-6;unit_text="(x1000000)"
    elif 100<ql*10**-5<1000:unit=10**-5;unit_text="(x100000)"
    elif 100<ql*10**-4<1000:unit=10**-4;unit_text="(x10000)"
    elif 100<ql*10**-3<1000:unit=10**-3;unit_text="(x1000)"
    elif 100<ql*10**-2<1000:unit=10**-2;unit_text="(x100)"
    elif 100<ql*10**-1<1000:unit=10**-1;unit_text="(x10)"
    elif 0<ql<1000:unit=1;unit_text=""
    bpline=[];ccline=[];mfline=[];geneidlist=[];xmax=int(ql*unit)+4;textlength=[]
    gene_line='    <path d="M 2,{} h {}"/>'
    gene_text='    <text x="{}" y="{}">{}</text>'
    x_position=int(ql*unit)+6
    mark='    <path d="M {},{} v {}"/>'
    mark_text='    <text x="{}" y="{}">{}</text>'
    start=0
    for ct,i in enumerate(alllist):
        for j in i:
            geneid=j[0].replace('"',"");length=int(j[1])*unit;xposition=2.5+length
            textlength.append(len(geneid))
            if start==0:
                bpline.append(gene_line.format(4,length))
                geneidlist.append(gene_text.format(xposition,4.25,geneid))
            else:
                yposition=2*start+4
                if ct==0:bpline.append(gene_line.format(yposition,length))
                elif ct==1:ccline.append(gene_line.format(yposition,length))
                elif ct==2:mfline.append(gene_line.format(yposition,length))
                geneidlist.append(gene_text.format(xposition,yposition+0.25,geneid))
            start+=1
    with open("./draw/draw_detail.svg","w") as f:
        ymax=2*(len(bpline)+len(ccline)+len(mfline))+4
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(xmax+max(textlength),ymax+4)
        marks=[mark.format(2+10*k,ymax,0.5) for k in range(int(ql*unit/10)+1)]
        marks_text=[mark_text.format(2+10*k,ymax+1.2,str(k*10)) for k in range(int(ql*unit/10)+1)]
        mark_l='  <g id="mark" stroke="#000000" stroke-width="0.06">\n'+"\n".join(marks)+"\n  </g>\n"
        markfont='  <g id="mark_text" fill="black" font-size="1" text-anchor="middle" font-family="Times New Roman">\n'+"\n".join(marks_text)+"\n  </g>\n"
        colorlista=["#8ecfc9","#ffbe7a","#fa7f6f","#82b0d2","#beb8dc","#2878b5","#9ac9db","#f8ac8c","#c82423","#ff8884","#14517c","#2f7fc1","#96c37d",
                    "#f3d266","#d8383a","#a9b8c6","#c497b2","#8e8bfe","#fe99a2","#934b43","#d76364","#ef7a6d","#63e398","#b1ce46","#f1d77e","#9394e7","#5f97d2","#9dc3e7","#a1a9d0","#f0988c","#b883d3","#c4a5de",
                    "#f6cae5","#96cccb"]
        colorlist=[]
        if singlecolor==False:
            if color=="":colorlist=random.sample(colorlista,3)
            else:
                colorlist=color.split(",")
                if len(colorlist)<3:colorlist=colorlist+random.sample(colorlista,3-len(colorlist))
        else:
            if color=="":colorlist.append(random.choice(colorlista));colorlist=colorlist*3
            else:
                coloru=color.split(",")[0]
                if coloru=="":coloru=random.choice(colorlista)
                colorlist.append(coloru)
                colorlist=colorlist*3
        query_color=colorlist[0]
        bp_segment='  <g id="BP" stroke="{}" stroke-width="1">\n'.format(query_color)+"\n".join(bpline)+"\n  </g>\n"
        if bpline!=[]:
            bp_sig='  <g id="BPsig" stroke="{}" stroke-width="1">\n'.format(query_color)+'    <path d="M {},{} h {}"/>'.format(x_position,ymax-2,2)+"\n  </g>\n"
            bp_text='  <g id="bp_text" fill="black" font-size="1" font-family="Times New Roman">\n'+'    <text x="{}" y="{}">biological process</text>\n'.format(x_position+3,ymax-1.75)+'    <text x="{}" y="{}">{}</text>'.format(x_position,ymax+1.2,unit_text)+"\n  </g>\n"
        else:bp_text="";bp_sig=""
        y_label='  <text x="{}" y="{}"  font-size="1.5" font-family="Times New Roman">{}</text>\n'.format((x_position+2)/2,ymax+2.5,"gene number")
        query_color=colorlist[1]
        cc_segment='  <g id="CC" stroke="{}" stroke-width="1">\n'.format(query_color)+"\n".join(ccline)+"\n  </g>\n"
        if ccline!=[]:
            cc_sig='  <g id="CCsig" stroke="{}" stroke-width="1">\n'.format(query_color)+'    <path d="M {},{} h {}"/>'.format(x_position,ymax-4,2)+"\n  </g>\n"
            cc_text='  <g id="cc_text" fill="black" font-size="1" font-family="Times New Roman">\n'+'    <text x="{}" y="{}">cellular component</text>'.format(x_position+3,ymax-3.75)+"\n  </g>\n"
        else:cc_text="";cc_sig=""
        query_color=colorlist[2]
        mf_segment='  <g id="MF" stroke="{}" stroke-width="1">\n'.format(query_color)+"\n".join(mfline)+"\n  </g>\n"
        if mfline!=[]:
            mf_sig='  <g id="MFsig" stroke="{}" stroke-width="1">\n'.format(query_color)+'    <path d="M {},{} h {}"/>'.format(x_position,ymax-6,2)+"\n  </g>\n"
            mf_text='  <g id="mf_text" fill="black" font-size="1" font-family="Times New Roman">\n'+'    <text x="{}" y="{}">molecular function</text>'.format(x_position+3,ymax-5.75)+"\n  </g>\n"
        else:mf_text="";mf_sig=""
        text_target='  <g id="target_text" fill="black" font-size="1" font-family="Times New Roman">\n'+"\n".join(geneidlist)+"\n  </g>\n"
        y_axis='    <path d="M 2,2 v {}"/>'.format(ymax-2)
        x_axis='    <path d="M 2,{} h {}"/>'.format(ymax,int(ql*unit)+4)
        xy='  <g id="mark" stroke="#000000" stroke-width="0.06">\n'+y_axis+"\n"+x_axis+"  </g>\n"
        end='  </svg>'
        f.write(file_title+mark_l+markfont+bp_segment+bp_sig+cc_segment+cc_sig+mf_segment+mf_sig+bp_text+cc_text+mf_text+text_target+xy+y_label+end)

colors={"cy2bl":("#2af9df","#2dede2","#4affff","#34d5e8","#4affff","#3bbdef","#3eb2f2","#42a5f5","#459bf8","#4b84fe"),
        "lp2dp":("#ba77ea","#ae6fdd","#a066cf","#945ec2","#8756b5","#7a4ea8","#6d469b","#5f3d8d","#52357f","#3c2768"),
        "cy2p":("#5efae8","#5fefea","#62e1ec","#64d3ee","#66c2f0","#68b4f3","#6aa6f5","#6e89f9","#717cfb","#726ffd"),
        "rcy2cy":("#960acc","#8d1dd1","#8531d6","#7d44db","#7457e0","#6c6ce6","#5c90ef","#52a6f5","#4ab9fa","#43c9fe"),
        "cy2bb":("#51e1e6","#4bcee2","#45b8dd","#3ea2d8","#388dd3","#3276ce","#2b60c9","#254bc5","#1921bb","#140fb7"),
        "lcy2dcy":("#64fbef","#5dede7","#56dfe0","#4ed1d8","#47c2d0","#40b5c9","#39a6c1","#3299ba","#2a89b1","#237caa"),
        "lg2cy":("#67fe98","#5dfca2","#53f9ac","#48f6b7","#3ef4c1","#33f1cc","#29eed6","#1eebe1","#13e9eb","#09e6f5"),
        "lg2db":("#77efa4","#6de1a5","#63d2a5","#58c2a6","#4db4a7","#42a5a8","#3896a9","#2c87aa","#2278ab","#1769ac"),
        "r2cy":("#ee68b4","#e378ba","#d887c0","#cd96c6","#c2a5cc","#b7b4d2","#acc3d7","#a0d3de","#96e2e3","#8bf1e9"),
        "lg2db":("#8ffbbe","#82e7b5","#73d1ac","#64bba2","#56a699","#48918f","#397b86","#29647c","#1b4e72","#032b63"),
        "lb2db":("#94a9fd","#889ef3","#7b92e9","#6d86de","#607ad4","#536ec9","#4663c0","#3856b4","#2b4baa","#1b3d9e"),
        "r2g":("#f8056c","#f01c6c","#e7356b","#de4e6a","#d56869","#cc8268","#c39b68","#bab467","#b1cd66","#a9e465"),
        "y2b":("#e5cc7b","#d8bc83","#c9a98c","#ba9696","#ab839f","#9c70a8","#8d5db1","#7e48bb","#6f36c4","#5717d3"),
        "r2b":("#ec99e5","#dd93e7","#ce8de9","#bf88eb","#b182ed","#a17cef","#9377f1","#8371f3","#746bf5","#6565f7"),
        "yrp":("#ecca17","#e7b82d","#e1a743","#db935b","#d58173","#cf6d8b","#c95aa2","#c346bb","#bd33d2","#b418f4"),
        "y2cy":("#eefe02","#dff91b","#dff91b","#c1f04c","#b2eb66","#a2e680","#93e298","#83dcb3","#74d8cb","#66d3e3"),
        "y2p":("#efc775","#e8bb7b","#e0af82","#d9a288","#d1968f","#ca8996","#c37d9c","#bb71a3","#b464a9","#ac57b0"),
        "lr2dr":("#ed5d56","#dc5654","#c94d52","#b64450","#a23b4d","#91334b","#7f2b49","#6c2246","#6b2146","#4b4033"),
        "lpk2dpk":("#f5cbeb","#f3bee8","#efaee5","#eda0e2","#ea90df","#e782dc","#e781dc","#e472d9","#de54d2","#db45cf"),
        "y2pur":("#f6cf45","#f7c355","#f8b665","#f8a975","#f99d85","#fa9095","#fb83a6","#fc75b7","#fd69c6","#fe5cd8"),
        "pur2b":("#f6affe","#e19ffc","#cb8df9","#b47cf7","#9e6bf4","#8759f1","#7148ef","#5935ec","#4425ea","#2009e5"),
        "y2r":("#fcd418","#fac117","#f8ac14","#f69713","#f48210","#f26d0e","#f0580d","#ee420a","#ec2d09","#ea1806"),
        "dp2b":("#fb6dd7","#e965d5","#d55cd3","#c252d1","#ae49cf","#9940cd","#8637ca","#702dc8","#5d24c6","#491bc4"),
        "o2cy":("#fbcd72","#e6c57d","#d0bc88","#bbb392","#a4aa9d","#a5aa9d","#8ea1a8","#7998b2","#4d87c8","#2e7ad7"),
        "y2db":("#fbd803","#e5c60e","#ccb21b","#b49f27","#9c8b33","#847840","#6d654c","#524f5a","#3b3e65","#1a2376"),
        "y2o":("#ffe783","#fedc7b","#fed172","#fdc569","#fdb960","#fcad56","#fca14e","#fb9444","#fb8a3c","#fa7f33"),
        "y2lp":("#fdeeb1","#f8dbb9","#f3c7c0","#eeb2c9","#e99ed0","#e389d9","#de74e1","#d85fe9","#d34bf0","#cc2dfc"),
        "o2r":("#fff2b5","#fee2af","#fdd0a7","#fcbfa0","#fbad98","#fa9a91","#f98889","#f87481","#f7637a","#f6496f"),
        "y2g":("#fbf61f","#eaf31c","#d6f019","#c2ec16","#aee912","#9be50f","#88e20c","#73de09","#60db06","#4dd803")}

def differentlevel_go(total,min,current):
    unitlength=int((total-min)/10)+1
    if min<=current<min+unitlength:return 9
    elif min+unitlength<=current<min+unitlength*2:return 8
    elif min+unitlength*2<=current<min+unitlength*3:return 7
    elif min+unitlength*3<=current<min+unitlength*4:return 6
    elif min+unitlength*4<=current<min+unitlength*5:return 5
    elif min+unitlength*5<=current<min+unitlength*6:return 4
    elif min+unitlength*6<=current<min+unitlength*7:return 3
    elif min+unitlength*7<=current<min+unitlength*8:return 2
    elif min+unitlength*8<=current<min+unitlength*9:return 1
    elif min+unitlength*9<=current<min+unitlength*10:return 0

def colorbar_go(colortup,x,total,min):
    defcolor='  <defs>\n    <linearGradient id="viridis" x1="0%" y1="100%" x2="0%" y2="0%">\n      ' \
            '<stop offset="0%" stop-color="{}"/>\n      <stop offset="45%" stop-color="{}"/>\n      ' \
            '<stop offset="65%" stop-color="{}"/>\n      <stop offset="100%" stop-color="{}"/>\n    ' \
            '</linearGradient>\n  </defs>\n'
    rectext=defcolor.format(colortup[9],colortup[6],colortup[3],colortup[0])+'  <rect x="{}" y="{}" width="0.5" height="10" fill="url(#{})"/>\n'.format(x,2,"viridis")
    labeltext=[]
    textj='    <text x="{}" y="{}">{}</text>'
    unit=int((total-min)/10)+1
    for i in range(10):
        y=2+i;text=((10-i)*unit+min)*(-1)
        labeltext.append(textj.format(x+0.5,y+0.1,text))
    labeltext.append(textj.format(x,1.5,"gene number"))
    labeltext.append(textj.format(x,12.5,"BP:biological process"))
    labeltext.append(textj.format(x,13,"CC:cellular component"))
    labeltext.append(textj.format(x,13.5,"MF:molecular function"))
    texts='  <g id="target_text" fill="#000000" font-size="0.3" font-family="Times New Roman" text-anchor="start">\n'+"\n".join(labeltext)+"\n  </g>\n"
    result=rectext+texts
    return result

def heatmap_go(file,number,colormodel):
    gf={}
    allset={}
    ctgdir={"biological_process":1,"cellular_component":2,"molecular_function":3}
    with open(file,encoding="utf-8") as f:
        for line in f:
            if "Sorry" not in line:
                linelist=line.strip().split("\t")
                func=linelist[2].replace('"','');ctg=linelist[3]
                allset[func]=ctg
                if func not in gf:
                    gf[func]=1
                else:
                    gf[func]+=1
    lines=[];genetext=[];catetext=[]
    gene_line='    <path d="M {},{} h 1"  stroke="{}"/>'
    gene_text='    <text x="{}" y="{}">{}</text>'
    gf = {k: v for k, v in sorted(gf.items(), key=lambda item: item[1], reverse=True)}
    if number==0:bp=list(gf.items())[:]
    else:bp=list(gf.items())[:number]
    del gf
    maxnum=int(bp[0][1]);minmum=int(bp[-1][1])
    for i in range(0,len(bp),20):
        bps=bp[i:i+20]
        maxcurrent=max([int(len(j[0])/7)+1 for j in bps])
        ctgdir["biological_process"]=ctgdir["biological_process"]+maxcurrent
        ctgdir["cellular_component"]=ctgdir["cellular_component"]+maxcurrent
        ctgdir["molecular_function"]=ctgdir["molecular_function"]+maxcurrent
        text_x=ctgdir["biological_process"]
        for index,content in enumerate(bps):
            func=content[0];num=content[1]
            x=ctgdir[allset[func]];y=(index+2)*0.618
            color=colors[colormodel][differentlevel_go(maxnum,minmum,num)]
            line=gene_line.format(x,y,color)
            lines.append(line)
            text=gene_text.format(text_x-1,y+0.14,func)
            genetext.append(text)
        colorrange=colorbar_go(colors[colormodel],x+4,maxnum,minmum)
        ctgx=ctgdir["biological_process"]
        ctext=gene_text.format((2*ctgx+1)/2,y+1,"BP")
        catetext.append(ctext)
        ctext=gene_text.format((2*ctgx+3)/2,y+1,"CC")
        catetext.append(ctext)
        ctext=gene_text.format((2*ctgx+5)/2,y+1,"MF")
        catetext.append(ctext)
        ctgdir["biological_process"]=ctgdir["molecular_function"]+2
        ctgdir["cellular_component"]=ctgdir["molecular_function"]+3
        ctgdir["molecular_function"]=ctgdir["molecular_function"]+4
    with open("./draw/draw_detail.svg","w") as f:
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(ctgdir["molecular_function"]+4,14.8)
        line_content='  <g id="line_chr" stroke-width="0.618">\n'+"\n".join(lines)+"\n  </g>\n"
        genetext='  <g id="target_text" fill="#000000" font-size="0.3" font-family="Times New Roman" text-anchor="end">\n'+"\n".join(genetext)+"\n  </g>\n"
        ctgtext='  <g id="target_text" fill="#ff0000" font-size="0.3" font-family="Times New Roman" text-anchor="middle">\n'+"\n".join(catetext)+"\n  </g>\n"
        end='  </svg>'
        f.write(file_title+line_content+genetext+ctgtext+colorrange+end)

def drawkp(file,cutvalue,color,gene_number,singlecolor=1):
    colorlista=["#8ecfc9","#ffbe7a","#fa7f6f","#82b0d2","#beb8dc","#2878b5","#9ac9db","#f8ac8c","#c82423","#ff8884","#14517c","#2f7fc1","#96c37d",
                        "#f3d266","#d8383a","#a9b8c6","#c497b2","#8e8bfe","#fe99a2","#934b43","#d76364","#ef7a6d","#63e398","#b1ce46","#f1d77e","#9394e7","#5f97d2","#9dc3e7","#a1a9d0","#f0988c","#b883d3","#c4a5de",
                        "#f6cae5","#96cccb"]
    if color=="":
        if singlecolor==0:
            if cutvalue!=0:
                color=[]
                for i in range(cutvalue):
                    r = lambda: random.randint(0,255)
                    t_color="#%02X%02X%02X" % (r(),r(),r())
                    color.append(t_color)
            else:color=random.choice(colorlista)
        else:color=random.choice(colorlista)
    elif color.count("#")>=1:
        if singlecolor==0:
            if color.count("#")==cutvalue:
                color=color.split(",")
            else:
                dif=cutvalue-color.count("#")
                color=color.split(",")+random.sample(colorlista,dif)
        else:
            color=color.split(",")[0]
    gf={}
    number=cutvalue
    with open(file,encoding="utf-8") as f:
        for line in f:
            if "Sorry" not in line:
                linelist=line.strip().split("\t")
                func=linelist[2].replace('"','')
                if func not in gf:
                    gf[func]=1
                else:
                    gf[func]+=1
    gf = {k: v for k, v in sorted(gf.items(), key=lambda item: item[1], reverse=True)}
    if number==0:
        bp=list(gf.items())[:]
    else:bp=list(gf.items())[:number]
    if gene_number!=0:
        bp=[i for i in bp if int(i[1])>gene_number]
    ql=int(bp[0][1])
    ymax=len(bp)*3+5
    if 100<ql*10**-6<1000:unit=10**-6;unit_text="(x1000000)"
    elif 100<ql*10**-5<1000:unit=10**-5;unit_text="(x100000)"
    elif 100<ql*10**-4<1000:unit=10**-4;unit_text="(x10000)"
    elif 100<ql*10**-3<1000:unit=10**-3;unit_text="(x1000)"
    elif 100<ql*10**-2<1000:unit=10**-2;unit_text="(x100)"
    elif 100<ql*10**-1<1000:unit=10**-1;unit_text="(x10)"
    elif 0<ql<1000:unit=1;unit_text=""
    lines=[];genetext=[];xmax=int(ql*unit)+5;textlength=[]
    gene_line='  <path d="M 2,{} h {}"  stroke="{}" stroke-width="1.5"/>'
    gene_text='    <text x="{}" y="{}">{}</text>'
    mark='    <path d="M {},{} v {}"/>'
    for index,i in enumerate(bp):
        if isinstance(color,list):
            t_color=color[index]
        else:t_color=color
        geneid,num=i
        y=3*index+5;length=int(num)*unit
        line=gene_line.format(y,length,t_color)
        lines.append(line)
        text=gene_text.format(2.5+length,y+0.25,geneid)
        genetext.append(text)
        textlength.append(len(geneid))
    marks=[mark.format(2+10*k,ymax,0.5) for k in range(int(ql*unit/10)+1)]
    marks_text=[gene_text.format(2+10*k,ymax+1.25,str(k*10)) for k in range(int(ql*unit/10)+1)]
    with open("./draw/draw_detail.svg","w") as f:
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(xmax+max(textlength),ymax+4)
        genes="\n".join(lines)+"\n"
        genetext='  <g id="target_text" fill="#000000" font-size="1.5" font-family="Times New Roman" text-anchor="start">\n'+"\n".join(genetext)+"\n  </g>\n"
        mark_l='  <g id="mark" stroke="#000000" stroke-width="0.06">\n'+"\n".join(marks)+"\n  </g>\n"
        markfont='  <g id="mark_text" fill="black" font-size="1" text-anchor="middle" font-family="Times New Roman">\n'+"\n".join(marks_text)+"\n  </g>\n"
        x_line='  <path d="M 2,{} h {}"  stroke="{}" stroke-width="0.1"/>'
        x_axis=x_line.format(ymax,int(ql*unit)+1,"black")+"\n"
        y_axis='  <path d="M 2,2 v {}"  stroke="black" stroke-width="0.06"/>\n'.format(ymax-2)
        unit_sig='  <text x="{}" y="{}" font-size="1" text-anchor="start">{}</text>\n'.format(int(ql*unit)+1,ymax+1.25,unit_text)
        x_label='  <text x="{}" y="{}"  font-size="1.5" font-family="Times New Roman">{}</text>\n'.format((int(ql*unit/10)*5+2),ymax+2.5,"gene number")
        end='  </svg>'
        f.write(file_title+genes+genetext+mark_l+markfont+x_axis+y_axis+unit_sig+x_label+end)

def colorbar_kegg(colortup,x,total,min):
        defcolor='  <defs>\n    <linearGradient id="viridis" x1="0%" y1="100%" x2="0%" y2="0%">\n      ' \
                '<stop offset="0%" stop-color="{}"/>\n      <stop offset="45%" stop-color="{}"/>\n      ' \
                '<stop offset="65%" stop-color="{}"/>\n      <stop offset="100%" stop-color="{}"/>\n    ' \
                '</linearGradient>\n  </defs>\n'
        rectext=defcolor.format(colortup[9],colortup[6],colortup[3],colortup[0])+'  <rect x="{}" y="{}" width="0.5" height="10" fill="url(#{})"/>\n'.format(x,2,"viridis")
        labeltext=[]
        textj='    <text x="{}" y="{}">{}</text>'
        unit=int((total-min)/10)+1
        for i in range(10):
            y=2+i;text=((10-i)*unit+min)*(-1)
            labeltext.append(textj.format(x+0.5,y+0.1,text))
        texts='  <g id="target_text" fill="#000000" font-size="0.3" font-family="Times New Roman" text-anchor="start">\n'+"\n".join(labeltext)+"\n  </g>\n"
        gn='  <text x="{}" y="{}" fill="#ff0000" font-size="0.5" font-family="Times New Roman" text-anchor="start">{}</text>\n'.format(x,1.6,"gene number")
        result=rectext+texts+gn
        return result

def heatmap_kegg(file,number,colormodel):
    gf={}
    allset=set()
    with open(file,encoding="utf-8") as f:
        for line in f:
            if "Sorry" not in line:
                linelist=line.split("\t")
                func=linelist[1]#kegg id
                if func not in gf:
                    gf[func]=1
                else:
                    gf[func]+=1
    lines=[];genetext=[];yadd=[];catetext=[]
    gene_line='    <path d="M {},{} h 1"  stroke="{}"/>'
    gene_text='    <text x="{}" y="{}">{}</text>'
    ko_text='    <text transform="translate({},{}) rotate(-90)">{}</text>'
    gf = {k: v for k, v in sorted(gf.items(), key=lambda item: item[1], reverse=True)}
    with gzip.open("./kegg/KEGG2KO.txt.gz","rt") as f1:
        content=f1.readline()
        K_ko_file_content = json.loads(content)
        for index,content in enumerate(gf):
            if index<number:
                allset=allset|set(K_ko_file_content[content])
    with gzip.open("./kegg/keggfunc.txt.gz","rt") as f:
        content=f.readline()
        Keggfunc = json.loads(content)
    with gzip.open("./kegg/KOfunction.txt.gz","rt") as f:
        content=f.readline()
        Kofunc = json.loads(content)
    bp=list(gf.items())[:number]
    ymax=(len(bp)+4)*0.618
    bpdir={x[0]:int(x[1]) for x in bp}
    del gf
    maxnum=int(bp[0][1]);minnum=int(bp[-1][1])
    maxcurrent_unit=max([int(len(j[0])/3)+1 for j in bp])+6#单位值，每一个x都要加上这个值，以保证x的值都在y轴右侧
    xmax=len(allset)+2*maxcurrent_unit
    xps={i:index+maxcurrent_unit for index,i in enumerate(allset)}#得到了关于ko ID的横坐标
    yps={j[0]:(index+2)*0.618 for index,j in enumerate(bp)}#得到了关于kegg ID的y坐标
    for ID,yp in yps.items():
        text=gene_text.format(maxcurrent_unit-0.2,yp,Keggfunc[ID])
        genetext.append(text)
        for x in K_ko_file_content[ID]:
            xp=xps[x]
            color=colors[colormodel][differentlevel_go(maxnum,minnum,bpdir[ID])]
            line=gene_line.format(xp,yp,color)
            lines.append(line)
    for key,content in xps.items():
        textko=Kofunc[key]
        yadd.append(int(len(textko)/6))
        kotext=ko_text.format((2*content+1)/2,yp+1,textko)
        catetext.append(kotext)
    colorrange=colorbar_kegg(colors[colormodel],(2*content+1)/2+4,maxnum,minnum)
    with open("./draw/draw_detail.svg","w") as f:
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(xmax,ymax+max(yadd))
        line_content='  <g id="line_chr" stroke-width="0.618">\n'+"\n".join(lines)+"\n  </g>\n"
        genetext='  <g id="kegg_text" font-size="0.3" font-family="Times New Roman" text-anchor="end" dominant-baseline="middle">\n'+"\n".join(genetext)+"\n  </g>\n"
        ctgtext='  <g id="ko_text" font-size="0.3" font-family="Times New Roman" text-anchor="end">\n'+"\n".join(catetext)+"\n  </g>\n"
        kegg_text='  <text x="{}" y="0.5" font-size="0.5" font-family="Times New Roman" fill="#ff0000"  text-anchor="end">KEGG functions</text>\n'.format(maxcurrent_unit-0.2)
        kO_text='  <text transform="translate({},{}) rotate(-90)" font-size="0.5" font-family="Times New Roman" fill="#ff0000"  text-anchor="end">KO functions</text>\n'.format(maxcurrent_unit,yp+1)
        end='  </svg>'
        f.write(file_title+line_content+genetext+ctgtext+kegg_text+kO_text+colorrange+end)

def heatmap_pfam(file,number,colormodel):
    gf={}
    with open(file,encoding="utf-8") as f:
        for line in f:
            if "Sorry" not in line:
                linelist=line.strip().split("\t")
                func=linelist[2]#kegg id
                if func not in gf:
                    gf[func]=1
                else:
                    gf[func]+=1
    lines=[];genetext=[];yadd=[]
    gene_line='    <path d="M {},{} h 1"  stroke="{}"/>'
    gene_text='    <text x="{}" y="{}">{}</text>'
    gf = {k: v for k, v in sorted(gf.items(), key=lambda item: item[1], reverse=True)}
    bp=list(gf.items())[:number]
    del gf
    maxnum=int(bp[0][1]);minnum=int(bp[-1][1])
    groupnumber=int(len(bp)/20)+1
    for i in range(groupnumber):
        smallrange=bp[i*20:(i+1)*20]
        funclength=i*10+10
        for index,content in enumerate(smallrange):
            genetext.append(gene_text.format(funclength,index+1.6,content[0]))
            yadd.append(index+1.6)
        for index,content in enumerate(smallrange):
            lines.append(gene_line.format(funclength+0.2,index+1.6,colors[colormodel][differentlevel_go(maxnum,minnum,content[1])]) )
    xmax=funclength+10
    ymax=max(yadd)+1.6
    colorrange=colorbar_kegg(colors[colormodel],funclength+2,maxnum,minnum)
    with open("./draw/draw_detail.svg","w") as f:
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(xmax,ymax)
        line_content='  <g id="line_chr" stroke-width="0.618">\n'+"\n".join(lines)+"\n  </g>\n"
        genetext='  <g id="kegg_text" font-size="0.3" font-family="Times New Roman" text-anchor="end" dominant-baseline="middle">\n'+"\n".join(genetext)+"\n  </g>\n"
        end='  </svg>'
        f.write(file_title+line_content+genetext+colorrange+end)

def drawstatistics(file,cut_value,drawtype,color,colormodel,gene_number,singlecolor=False,go=False,kegg=False,multi_families=False):
    if singlecolor==True:singlecolor=1
    else:singlecolor=0
    cutvalue=cut_value
    filepath=file
    if go:
        if drawtype=="bar chart":
            drawgo(filepath,cutvalue,color,gene_number,singlecolor)
        if drawtype=="heatmap":
            heatmap_go(file,cutvalue,colormodel)
        if drawtype=="select draw type   ":
            drawgo(filepath,cutvalue,color,gene_number)
    elif kegg:
        if drawtype=="bar chart":
            drawkp(filepath,cutvalue,color,gene_number,singlecolor)
        if drawtype=="heatmap":
            heatmap_kegg(file,cutvalue,colormodel)
        if drawtype=="select draw type   ":
            drawkp(filepath,cutvalue,color,gene_number,singlecolor)
    elif multi_families:
        if drawtype=="bar chart":
            drawkp(filepath,cutvalue,color,gene_number,singlecolor)
        if drawtype=="heatmap":
            heatmap_pfam(file,cutvalue,colormodel)
        if drawtype=="select draw type   ":
            drawkp(filepath,cutvalue,color,gene_number,singlecolor)

def save_drawstatis(savetype):
        file="./draw/draw_detail.svg"
        drawing = svg2rlg(file)
        if savetype=="pdf":
            savename=file+".pdf"
            renderPDF.drawToFile(drawing, savename)

def numr(minn,maxn,currentnum):
    global radio
    unit=int((maxn-minn)/10)+1
    if minn<=currentnum<minn+unit:radio=2
    elif minn+unit<=currentnum<minn+unit*2:radio=2.5
    elif minn+unit*2<=currentnum<minn+unit*3:radio=3
    elif minn+unit*3<=currentnum<minn+unit*4:radio=5.5
    elif minn+unit*4<=currentnum<minn+unit*5:radio=6
    elif minn+unit*5<=currentnum<minn+unit*6:radio=6.5
    elif minn+unit*6<=currentnum<minn+unit*7:radio=7
    elif minn+unit*7<=currentnum<minn+unit*8:radio=8
    elif minn+unit*8<=currentnum<minn+unit*9:radio=9
    elif minn+unit*9<=currentnum<minn+unit*10:radio=10
    return radio

def numrp(minn,maxn,currentnum):
    global radio
    unit=int(maxn/minn)/10+1;cur=int(currentnum/minn)
    if 1<=cur<unit:radio=1
    elif unit<=cur<unit*2:radio=2
    elif unit*2<=cur<unit*3:radio=3
    elif unit*3<=cur<unit*4:radio=4
    elif unit*4<=cur<unit*5:radio=5
    elif unit*5<=cur<unit*6:radio=6
    elif unit*6<=cur<unit*7:radio=7
    elif unit*7<=cur<unit*8:radio=8
    elif unit*8<=cur<unit*9:radio=9
    elif unit*9<=cur<unit*10:radio=10
    return radio

def colorbar_allrevigo(colortup,minn,maxn,x=560):
    defcolor='  <defs>\n    <linearGradient id="viridis" x1="0%" y1="100%" x2="0%" y2="0%">\n      ' \
            '<stop offset="0%" stop-color="{}"/>\n      <stop offset="45%" stop-color="{}"/>\n      ' \
            '<stop offset="65%" stop-color="{}"/>\n      <stop offset="100%" stop-color="{}"/>\n    ' \
            '</linearGradient>\n  </defs>\n'
    rectext=defcolor.format(colortup[0],colortup[3],colortup[6],colortup[9])+'  <rect x="{}" y="{}" width="4" height="100" fill="url(#{})"/>\n'.format(x,50,"viridis")
    labeltext=[];circles=[];labeltext2=[]
    textj='    <text x="{}" y="{}">{}</text>'
    circle='    <circle cx="{}" cy="{}" r="{}"/>'
    for index,i in enumerate(["-0.05","-0.0375","-0.025","-0.0125","- 0"]):
        y=50+index*25
        labeltext.append(textj.format(x+3.8,y+1.3,i))
    unit=int((maxn-minn)/10)+1
    for i in range(4):
        rlist=[2,5.5,7,10];ylist=[175,185.5,201,221];textsl=[minn,minn+unit*3,minn+unit*6,minn+unit*9]
        circles.append(circle.format(x,ylist[i],rlist[i]))
        labeltext.append(textj.format(x+11,ylist[i]+2,textsl[i]))
    labeltext2.append(textj.format(x+4,168,"gene number"))
    labeltext2.append(textj.format(x+4,45,"p-value"))
    texts='  <g id="target_text" fill="#000000" font-size="5" font-family="Times New Roman" text-anchor="start">\n'+"\n".join(labeltext)+"\n  </g>\n"
    gn='  <g id="target_text2" fill="#ff0000" font-size="6" font-family="Times New Roman" text-anchor="middle">\n'+"\n".join(labeltext2)+"\n  </g>\n"
    cg='  <g id="circlemodel" stroke="#000000" stroke-width="0.5" fill="#ffffff">\n'+"\n".join(circles)+"\n  </g>\n"
    result=rectext+cg+texts+gn
    return result

def allrevigo(speciesname,number_threshold,threshold,filename,func,numberthreshold,rmodel,network=False,go=False,kegg=False,pfam=False):
    speciesdir={}
    if speciesname!="select closely related species":
        if go:
            speciesname="./go/go_p/"+speciesname
        elif kegg:
            speciesname="./kegg/kegg_p/"+speciesname
        elif pfam:
            speciesname="./pfam/pfam_p/"+speciesname
        referencename=speciesname+".txt.gz"
        with gzip.open(referencename,"rt") as f:
            content=f.readline()
            speciesdir = json.loads(content)
    if number_threshold=="":number_threshold=20#展示数量为前20%的
    else:number_threshold=int(number_threshold)
    if threshold=="":threshold=0.05
    else:threshold=float(threshold)
    if go==False:func=""
    with open(filename,encoding="utf-8") as f:
        godir={}
        for number,line in enumerate(f):
            if func in line and "Sorry" not in line and "#" not in line:
                goid=line.split("\t")[1]
                if goid not in godir:
                    godir[goid]=1
                else:godir[goid]+=1
    currentnumber=number
    if number_threshold>100:number_threshold=100
    number_threshold=int(len(godir)*number_threshold/100)+1
    nvaluesort=sorted(godir.items(),key=lambda item:item[1],reverse=True)[:number_threshold]#根据设定的阈值排序后切割
    del godir
    if numberthreshold=="":numberthreshold=0
    else:numberthreshold=float(numberthreshold)
    godir={x:y for x,y in nvaluesort if y>=numberthreshold}#存储ID和数量
    goorkegg=nvaluesort[0][0]#通过这个变量去区分输入的是kegg还是go结果
    connectionfile=""
    if "GO:" in goorkegg:
        goandfunc="./go/go_func.txt.gz"
        connectionfile="./go/go_connect.txt.gz"
    elif "K" in goorkegg:
        goandfunc="./kegg/keggfunc.txt.gz"
        connectionfile="./kegg/kegg_connect.txt.gz"
    elif "PF" in goorkegg:
        goandfunc="./pfam/pfamfunc.txt.gz"
    with gzip.open(goandfunc,"rt") as f:
        content=f.readline()
        gofunc = json.loads(content)
    if connectionfile!="":
        with gzip.open(connectionfile,"rt") as f:
            content=f.readline()
            connectionship=json.loads(content)
    if speciesname!="select closely related species" and speciesdir!={}:
        allnumber=int(speciesdir["total_number"])
        evaluedir={}#提供的是各个ID的pvalue
        for ID,number1 in godir.items():
            if ID in speciesdir:
                number2=int(speciesdir[ID])
                pvalue=scipy.stats.fisher_exact([[number1,currentnumber],[number2,allnumber]])[1]
                if pvalue<=threshold:
                    evaluedir[ID]=pvalue#存储ID和pvalue，同时这里存储的是最后要展示在图中的ID
    else:
        evaluedir={ID:0 for ID in godir}
    positiondir={goid:random.sample(range(50,500),2) for goid in evaluedir}#将ID与坐标相关
    pvaluelist=[];pmin=0;pmax=0;plist=[]
    if speciesname!="select closely related species":
        pvaluelist=[value for value in evaluedir.values()]
    if pvaluelist!=[]:
        pmin=min(pvaluelist);pmax=max(pvaluelist)
    numrange=[godir[ID] for ID in evaluedir]
    num_min=min(numrange);num_max=max(numrange)
    id_r={ID:numr(num_min,num_max,godir[ID]) for ID in evaluedir}#将ID与半径相关
    if pmin!=0:plist={ID:numrp(pmin,pmax,current) for ID,current in evaluedir.items()}
    if rmodel=="select colormodel   ":rmodel="r2cy"
    cb=colorbar_allrevigo(colors[rmodel],num_min,num_max)
    circle_list=[]
    circle='    <circle cx="{}" cy="{}" r="{}" stroke="#ffffff" stroke-width="{}" fill="{}"/>\n'
    text='    <text x="{}" y="{}" font-size="{}">{}</text>'
    line='    <path d="M {},{} L {},{}"/>'
    if plist!=[]:circle_list=[circle.format(positiondir[i][0],positiondir[i][1],r,r/20,colors[rmodel][int((plist[i])-1)]) for i,r in id_r.items()]
    else:circle_list=[circle.format(positiondir[i][0],positiondir[i][1],r,r/20,colors[rmodel][0]) for i,r in id_r.items()]
    if "K" in goorkegg:
        circle_text=[text.format(positiondir[i][0],positiondir[i][1],r,gofunc[i])  for i,r in id_r.items()]
    else:
        circle_text=[text.format(positiondir[i][0],positiondir[i][1],r,gofunc[i].split("\t")[1])  for i,r in id_r.items()]
    dir_connection={}
    if connectionfile!="":
        for GOid in id_r:
            if GOid in connectionship:
                cts=connectionship[GOid]
                for j in cts:
                    if j not in dir_connection:
                        dir_connection[j]=set()
                    dir_connection[j].add(GOid)
        file=open("./detail_information.txt","w")
        print("#ID\tfunction\tgene number\tp-value",file=file)
        for gosl in dir_connection.values():
            if len(gosl)>=2:
                if "GO:" in goorkegg:
                    [print("\t".join(gofunc[content].split("\t")[:2])+"\t"+str(godir[content])+"\t"+str(evaluedir[content]),file=file) for content in gosl]
                    print("#",file=file)
                elif "K" in goorkegg:
                    [print(content+"\t"+gofunc[content]+"\t"+str(godir[content])+"\t"+str(evaluedir[content]),file=file) for content in gosl]
                    print("#",file=file)
        file.close()
    with open("./draw/draw_detail.svg","w") as f:
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(600,550)
        circles="".join(circle_list)
        markfont='  <g id="mark_text" fill="black" text-anchor="middle" font-family="Times New Roman">\n'+"\n".join(circle_text)+"\n  </g>\n"
        end='  </svg>'
        f.write(file_title+circles+markfont+cb+end)
    if network:draw_path(colormodel)

def colorbar_path(colortup,minn,maxn,ymax,x=580):
        defcolor='  <defs>\n    <linearGradient id="viridis" x1="0%" y1="100%" x2="0%" y2="0%">\n      ' \
                '<stop offset="0%" stop-color="{}"/>\n      <stop offset="45%" stop-color="{}"/>\n      ' \
                '<stop offset="65%" stop-color="{}"/>\n      <stop offset="100%" stop-color="{}"/>\n    ' \
                '</linearGradient>\n  </defs>\n'
        rectext=defcolor.format(colortup[0],colortup[3],colortup[6],colortup[9])+'  <rect x="{}" y="{}" width="3" height="{}" fill="url(#{})"/>\n'.format(x+0.2,10,(ymax/2),"viridis")
        labeltext=[];circles=[];labeltext2=[]
        textj='    <text x="{}" y="{}">{}</text>'
        circle='    <circle cx="{}" cy="{}" r="{}"/>'
        for index,i in enumerate(["-0.05","-0.0375","-0.025","-0.0125","- 0"]):
            y=10+index*(ymax/2)/5
            labeltext.append(textj.format(x+3.1,y+0.9,i))
        unit=int((maxn-minn)/10)+1
        for i in range(4):
            rlist=[1,1.4,2,2.6];ylist=[ymax/2+18,ymax/2+26,ymax/2+36,ymax/2+46];textsl=[minn,minn+unit*3,minn+unit*6,maxn]
            circles.append(circle.format(x,ylist[i],rlist[i]))
            labeltext.append(textj.format(x+4,ylist[i]+1,textsl[i]))
        labeltext2.append(textj.format(x+4,ymax/2+13,"gene number"))
        labeltext2.append(textj.format(x+4,6,"p-value"))
        texts='  <g id="target_text" fill="#000000" font-size="3" font-family="Times New Roman" text-anchor="start">\n'+"\n".join(labeltext)+"\n  </g>\n"
        gn='  <g id="target_text2" fill="#ff0000" font-size="4" font-family="Times New Roman" text-anchor="middle">\n'+"\n".join(labeltext2)+"\n  </g>\n"
        cg='  <g id="circlemodel" stroke="#000000" stroke-width="0.25" fill="#ffffff">\n'+"\n".join(circles)+"\n  </g>\n"
        result=texts+rectext+cg+gn
        return result

def numr_path(minn,maxn,currentnum):#注意以下两个函数在最终的程序里是可以重复利用的
    global radio
    unit=int((maxn-minn)/10)+1
    if minn<=currentnum<minn+unit:radio=1
    elif minn+unit<=currentnum<minn+unit*2:radio=1.2
    elif minn+unit*2<=currentnum<minn+unit*3:radio=1.4
    elif minn+unit*3<=currentnum<minn+unit*4:radio=1.6
    elif minn+unit*4<=currentnum<minn+unit*5:radio=1.8
    elif minn+unit*5<=currentnum<minn+unit*6:radio=2
    elif minn+unit*6<=currentnum<minn+unit*7:radio=2.2
    elif minn+unit*7<=currentnum<minn+unit*8:radio=2.4
    elif minn+unit*8<=currentnum<minn+unit*9:radio=2.6
    elif minn+unit*9<=currentnum<minn+unit*10:radio=2.8
    return radio

def draw_path(colormodel):
    with open("./detail_information.txt") as f:
        a=[line for line in f if "p-value" not in line and line!=""]
        lines="\n".join(a)
    modulars=lines.split("#")
    circle='    <circle cx="{}" cy="{}" r="{}" fill="{}"/>\n'
    text='    <text x="{}" y="{}" font-size="{}">{}</text>'
    line='    <path d="M {},{} L {},{}"/>'
    circles=[];texts=[];lines=[]
    xlistall=[];ylistall=[]#元素总个数
    alllength=[int(line.split("\t")[2]) for line in a if "#" not in line]
    minn=min(alllength);maxn=max(alllength)
    again1=[modular for modular in modulars if len(modular.strip().split("\n"))<50]
    again=[modular for modular in modulars if len(modular.strip().split("\n"))>=50]
    if again1!=[]:
        for index,modular in enumerate(again1):
            detailinfors=modular.strip().split("\n")
            if detailinfors!=['']:
                num=len(detailinfors)
                ybase=int(index/9);yrange=range(60*ybase+10,60*(ybase+1))
                xbase=index%9;xrange=range(56*xbase+52,102+56*xbase)
                xlist=random.sample(xrange,num);ylist=random.sample(yrange,num)
                xlistall+=xlist;ylistall+=ylist
                numlist=[int(line.split("\t")[2]) for line in detailinfors if line!=""]
                pvaluelist=[float(line.split("\t")[3]) for line in detailinfors if line!=""]
                idposition=[(xlist[index],ylist[index]) for index in range(num)]
                rlist=[numr_path(minn,maxn,current) for current in numlist]
                cminn=min(pvaluelist);cmaxn=max(pvaluelist)
                if cminn==0:cminn=1
                if colormodel=="select colormodel   ":colormodel="r2cy"
                plist=[numrp(cminn,cmaxn,current) for current in pvaluelist]
                c1=[circle.format(xlist[index],ylist[index],rlist[index],colors[colormodel][int((plist[index])-1)]) for index in range(num)]
                t1=[text.format(xlist[index],ylist[index],rlist[index],detail.split("\t")[1]) for index,detail in enumerate(detailinfors) if detail!=""]
                circles+=c1;texts+=t1
                for index,pos in enumerate(idposition):
                    x1,y1=pos
                    if index<=len(idposition)-2:
                        x2,y2=idposition[index+1]
                        lines.append(line.format(x1,y1,x2,y2))
    n=len(again1)
    if again!=[]:
        for index,modular in enumerate(again):
            ybase=index+int(n/9)+1;yrange=range(60*ybase+10,60*(ybase+1))
            xrange=range(52,550)
            random_list = list(itertools.product(xrange, yrange))
            detailinfors=modular.strip().split("\n")
            if detailinfors!=['']:
                num=len(detailinfors)
                allpos=random.sample(random_list,num)
                numlist=[int(line.split("\t")[2]) for line in detailinfors if line!=""]
                pvaluelist=[float(line.split("\t")[3]) for line in detailinfors if line!=""]
                rlist=[numr_path(minn,maxn,current) for current in numlist]
                cminn=min(pvaluelist);cmaxn=max(pvaluelist)
                if cminn==0:cminn=1
                if colormodel=="select colormodel   ":colormodel="r2cy"
                plist=[numrp(cminn,cmaxn,current) for current in pvaluelist]
                c2=[circle.format(allpos[index][0],allpos[index][1],rlist[index],colors[colormodel][(plist[index])-1]) for index in range(num)]
                t2=[text.format(allpos[index][0],allpos[index][1],rlist[index],detail.split("\t")[1]) for index,detail in enumerate(detailinfors) if detail!=""]
                circles+=c2;texts+=t2
                for index,pos in enumerate(allpos):
                    x1,y1=pos
                    if index<=len(allpos)-2:
                        x2,y2=allpos[index+1]
                        lines.append(line.format(x1,y1,x2,y2))
            xlist=[i[0] for i in allpos];ylist=[i[1] for i in allpos]
            xlistall+=xlist;ylistall+=ylist
    with open("./draw_network_detail.svg","w") as f:
        ymax=max(ylistall)
        yl=max([ymax/2+49,ymax+20])
        bar=colorbar_path(colors[colormodel],minn,maxn,ymax,x=max(xlistall)+32)
        file_title='<svg width="{}px" height="{}px" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(max(xlistall)+52,yl)
        circles="".join(circles)
        markfont='  <g id="mark_text" fill="black" text-anchor="middle" font-family="Times New Roman">\n'+"\n".join(texts)+"\n  </g>\n"
        connect='  <g id="connection" stroke="#f2f2f2" stroke-width="0.02">\n'+"\n".join(lines)+"\n  </g>\n"
        end='  </svg>'
        f.write(file_title+connect+circles+markfont+bar+end)


if __name__ == '__main__':
    args = argparseFunc()
    #if args.e==None:evalue="1e-5"在添加参数的时候会有一个default的选项所以不需要再额外指定
    evalue=args.e_value
    save=args.out;cpu=args.cpu#下面是功能注释的函数
    if (args.query_cds!=None or args.query_protein!=None) and (args.annotation_with_species!=None or args.annotation_with_database!=None):
        annotype=set()
        if args.query_cds!=None:inputtype="CDS";file=args.query_cds#支持cds与蛋白的输入
        elif args.query_protein!=None:inputtype="protein";file=args.query_protein
        if os.path.isfile(file)==False:#如果输入的仅仅只是序列，则在后台给它建个文件，所以老弟，前端一开始的那个输入框需要动一下，那个输入框接收的仅仅只是一个基因的序列
            with open("./target_seq.txt","w") as f:
                f.write(">target_seq\n"+file)
            file="./target_seq.txt"
        if args.alignment_model==None:algnment_type="fast"#有不同的比对模式
        else:algnment_type=args.alignment_model
        if args.alignment_percent==None:algnment_percent=80
        else:algnment_percent=args.alignment_percent
        only_ID=args.only_ID
        if args.go==args.kegg==args.pfam==False:#在这里收集的是注释类型
            annotype={"GO","KEGG","pfam"}
        else:
            if args.go:annotype.add("GO")
            if args.kegg:annotype.add("KEGG")
            if args.pfam:annotype.add("pfam")
        if args.annotation_with_species!=None:#第一种是使用近缘物种注释
            if args.annotation_with_species=="":refspecies="Arabidopsis_thaliana"
            else:refspecies=args.annotation_with_species
            align_annotation(file,inputtype,annotype,refspecies,evalue,algnment_type,algnment_percent,save,cpu,only_ID=None)
        if args.annotation_with_database!=None:#第二种是使用数据库注释
            databasetype=args.annotation_with_database
            if databasetype=="plant-special database":databasetype="psd"
            elif databasetype=="total database":databasetype="td"
            if databasetype=="psd" or databasetype=="td":
                plantannotate(file,evalue,save,inputtype,annotype,databasetype,cpu,only_ID=None)
            if databasetype=="nr" or databasetype=="swissprot":
                nr_swissprot(file,inputtype,databasetype,evalue,algnment_type,cpu,algnment_percent,save)#这里之后要改一下，结果只取相似度最高的那个
    if args.ncRNA_annotation:#当有这个参数的时候表示用户要对ncRNA进行注释
        filepath=args.query_cds;ncRNAtype=args.ncRNA_type
        identify_miRNA(filepath,save,evalue,cpu,ncRNAtype)
    if args.single_family:
        filepath=args.query_protein;model=args.model_name;model2=args.model_pathway
        if model==model2==None:print("please select a model for gene-family annotation or input the pathway of your interested model.")
        elif model!=None and model2==None:model2=""
        elif model==None and model2!=None:model=""
        singlefamily(filepath,model,save,cpu,evalue,model2=model2)
    if args.multi_families:
        filepath=args.query_protein
        if args.all_transcription_factor:
            model="alltf"
        elif args.all_gene_families:
            model="allgf"
        multifamilies(filepath,save,cpu,evalue,model)
    if args.translate:
        file=args.query_cds
        translatDNA(file,save)
    if args.RNA2DNA:
        file=args.query_cds
        rna2dna(file,save)
    if args.extract_infor:#在写参数的时候要写参数的完整名称，即--后面的内容
        file=args.annotation_result
        ID=args.ID
        if args.exfid:IDtype="fid"
        elif args.exgid:IDtype="gid"
        ext(file,save,ID,IDtype)
    if args.cf:
        file=args.genomic_result
        geneid=args.gid;goid=args.fid;pvalue=args.pvalue
        dealwithtranscriptome(file,save,geneid,goid,pvalue)
    if args.all_species:
        with open("./all_species.txt") as f:
            for line in f:print(line.strip())
    if args.all_families:
        with open("./all_families.txt") as f:
            for line in f:print(line.strip())
    if args.merge_result:
        if args.query_cds!=None:file=args.query_cds
        elif args.query_protein!=None:file=args.query_protein
        else:print("please input the pathway of protein or CDS file")
        pathway=args.results_pathway
        mergef(file,save,pathway)
    if args.draw_statistics:
        file=args.annotation_result
        cut_value=args.cut_value;drawtype=args.drawtypes;color=args.color;colormodel=args.colormodel;savetype=args.save_type
        gene_number=args.gene_number;singlecolor=args.singlecolor;go=args.go;kegg=args.kegg;multi_families=args.pfam
        if savetype==None:savetype="svg"
        if drawtype!="heatmap" or drawtype!="bar chart":drawtype="select draw type   "
        if color==None:color=""
        drawstatistics(file,cut_value,drawtype,color,colormodel,gene_number,singlecolor=singlecolor,go=go,kegg=kegg,multi_families=multi_families)
        save_drawstatis(savetype)
    if args.draw_network:
        speciesname=args.annotation_with_species
        number_threshold=args.cut_value
        threshold=args.pvalue
        filename=args.annotation_result
        func=args.go_category
        numberthreshold=args.gene_number
        rmodel=args.colormodel;go=args.go;kegg=args.kegg;multi_families=args.pfam
        allrevigo(speciesname,number_threshold,threshold,filename,func,numberthreshold,rmodel,network=True,go=go,kegg=kegg,pfam=multi_families)


        


