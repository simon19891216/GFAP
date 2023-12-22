<h1 align="center">GFAP: ultrafast and accurate gene functional annotation software for plants</h1>
<div align="center">
  <span class="author-block">
  <a href="">Dong Xu</a><sup>1,2*</sup>,</span>
  <span class="author-block">
    <a href="">Yingxue Yang</a><sup>1*</sup>,</span>
  <span class="author-block">
    <a href="">Desheng Gong</a><sup>1*</sup>,
  </span>
  <span class="author-block">
    <a href=" ">Xiaojian Chen</a><sup>1*</sup>
  </span>
  <span class="author-block">
    <a href=" ">Kangming Jin</a><sup>1</sup>
  </span>
  <span class="author-block">
    <a href=" ">Heling Jiang</a><sup>1</sup>
  </span>
  <span class="author-block">
    <a href=" ">Wenjuan Yu</a><sup>1</sup>
  </span>
  <span class="author-block">
    <a href=" ">Jihong Li</a><sup>1†</sup>
  </span>
  <span class="author-block">
    <a href=" ">Jin Zhang</a><sup>1†</sup>
  </span>
  </span>
  <span class="author-block">
    <a href=" ">Weihua Pan</a><sup>1†</sup>
  </span>
</div>
<div align="center">
  <span class="author-block"><sup>1</sup>
    Shenzhen Branch, Guangdong Laboratory of Lingnan Modern Agriculture, Genome Analysis Laboratory of the Ministry of Agriculture and Rural Affairs, Agricultural Genomics Institute at Shenzhen, Chinese Academy of Agricultural Sciences, Shenzhen 518120, China
  </span><br> 
  <span class="author-block"><sup>2</sup>State Key Laboratory of Subtropical Silviculture, College of Forestry and Biotechnology, Zhejiang A&F University, Hangzhou, Zhejiang 311300, China</span><br> 
  <span class="author-block"><sup>3</sup>
    School of Computer and Electronic Information/School of Artificial Intelligence, Nanjing Normal University, Nanjing 210023, China
  </span><br> 
  <span class="author-block"><sup>4</sup>
    State Key Laboratory of Plant Physiology and Biochemistry, College of Life Science, Zhejiang University, Hangzhou 310058, China
  </span><br> 
  <span class="author-block"><sup>5</sup>
    College of Forestry, Shandong Agricultural University, Tai'an, Shandong 271018, China
  </span><br> 
  <span class="author-block"><sup>*</sup>These authors contributed equally</a>, <sup>†</sup>Corresponding Authors </span><br> 
</div>

[![paper](https://img.shields.io/badge/Paper-Plant%20Physiology-green?style=flat-square)](https://doi.org/10.1093/plphys/kiad393)  [![website](https://img.shields.io/badge/GFAP-website-blue?logo=Github&style=flat-square)](http://43.139.112.84/go-kegg-pfam-index) 

a software for annotating genes, especially for annotating plant genes.

The software can be downloaded in the "Releases" module of this website. Furthermore, large amounts of toturials (including videos and manual) can also be found in this website, which can help users run GFAP without any barriers. 

The source code of GFAP has been uploaded into the 'Release' module. Please note that the source code is licensed under the BSD 3-Clause "NEW" or "Revised" License.

If the source code is helpful to your researches, please cite our article. Thank you!
## Contact
If you have any questions or suggestions about GFAP, please don't hesitate to contact me at xudongzhuanyong@163.com.
## Citation
If you find our work useful, please consider citing:

```
@article{10.1093/plphys/kiad393,
    author = {Xu, Dong and Yang, Yingxue and Gong, Desheng and Chen, Xiaojian and Jin, Kangming and Jiang, Heling and Yu, Wenjuan and Li, Jihong and Zhang, Jin and Pan, Weihua},
    title = "{GFAP: ultrafast and accurate gene functional annotation software for plants}",
    journal = {Plant Physiology},
    volume = {193},
    number = {3},
    pages = {1745-1748},
    year = {2023},
    doi = {10.1093/plphys/kiad393}
} 
```
## Interface and corresponding linux commands
### GO/KEGG/pfam：
#### annotate command 1:
```
pythonGFAP-linux.py
-qp/qn User input file or content
-aws user-selected content
-go/kegg/pfam (This is a multiple choice, depending on the user's selection, this will also be -go -kegg -pfam)
-am (fast or sensitive or do not set this option)
-e The value set by the user (Evalue can be set or not)
-ap The value set by the user (match-percentage can be set or not)
-only_ID (can be set or not)
-o The saved folder (if the previous one is a multi-selection, multiple result files will be generated at the same time, so it should be the path of a folder, and then all the results in this folder will be sent to the user. After the sending is completed Delete Files)
```

#### annotate command 2:
```
pythonGFAP-linux.py
-qp/qn User input file or content
-awd user-selected content
-go/kegg/pfam (This is a multiple choice, depending on the user's selection, this will also be -go -kegg -pfam)
-am (fast or sensitive or do not set this option)
-e The value set by the user (Evalue can be set or not)
-ap The value set by the user (match-percentage can be set or not)
-only_ID (can be set or not)
-o The saved folder (if the previous one is a multi-selection, multiple result files will be generated at the same time, so it should be the path of a folder, and then all the results in this folder will be sent to the user. After the sending is completed Delete Files)
```

###miRNA-lncRNA:
```
pythonGFAP-linux.py
-na
-nt (divided into miRNA or lncRNA according to user selection)
-qn user input file
-o The saving path of the result file, which will be sent to the user after completion (you can consider deleting it after the sending is completed, which will not be described in details below).
``` 

### gene families:
#### show members of a single family command
```
pythonGFAP-linux.py
-sf //single family
-qp (input file)
-mn/mp (Here you need to check whether there is a file put in mp. If there is a file put in, the parameter there is mp and the input file is added. If not, it is mn and the content selected by the user is added)
-o (save path of the result file, the processing method is the same as before)
```

#### show genes containing domains of families command
```
pythonGFAP-linux.py
-mf // domains of families
-atf/agf (screening for transcription factor/non-transcription factor families)
-qp (input file)
-o (save path of result file)
```

### statistics:
```
pythonGFAP-linux.py
-ds //draw statistics
-ar (input file)
-cut_value (there is a default value, the user can set it or not, the same as below)
-gn (has a default value, the user can set it or not)
-drawtypes (value)
-colormodel (value)
-color (value)
-singlecolor
-st (take value)
-go/-kegg/pfam
-o (will save the results to: ./draw/)
```

### pathway:
```
pythonGFAP-linux.py
-dn
-ar (input file)
-cut_value (there is a default value, the user can set it or not, the same as below)
-gn (has a default value, the user can set it or not)
-pvalue (there is a default value, the user can set it or not)
-colormodel (value)
-aws (receive value)
-st (take value)
-gca (receive value)
-go/kegg/pfam
-o (will save the results to: ./draw/)
``` 

### translation:
```
pythonGFAP-linux.py
-t
-qn (input file)
-o (save path of result file, same as above)
```

### RNA2DNA：
```
pythonGFAP-linux.py
-rd
-qn (input file)
-o (save path of result file, same as above)
```

### extraction:
#### extraction command
```
pythonGFAP-linux.py
-ex
-ar (input file)
-ID (ID or ID file)
-exfid/exgid (choose one)
-o (save path of result file, same as above)
```

#### merge annotation results
```
pythonGFAP-linux.py
-mr
-qn (input file)
-rp (You need to put the previous results into an empty folder and enter the location of the folder here. Be careful not to change the file name when moving the file)
-o (save path of result file, same as above)
``` 

### conversion：
```
pythonGFAP-linux.py
-cf
-gf (input file)
-gid (the index of the gene ID in the result file, received is an integer)
-fid (the index of go/pfam/kegg in the result file, receiving an integer)
-pvalue (the index of pvalue in the result file, receives an integer)
-o (the saving path of the result file, the processing of the results is the same as above)
```