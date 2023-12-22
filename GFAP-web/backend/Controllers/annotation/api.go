package annotation

import (
	"backend/Utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"regexp"
	"strings"
)

type Body struct {
	AlignmentMode   string   `json:"alignment_mode"`
	AnnotationType  []string `json:"annotation_type"`
	Database        string   `json:"database"`
	EValue          string   `json:"evalue"`
	GeneSequence    string   `json:"gene_sequence"`
	GeneSequence1   string   `json:"gene_sequence1"`
	MatchPercentage string   `json:"match_percentage"`
	InputType       string   `json:"input_type"`
	SequenceType    string   `json:"sequence_type"`
	FactorType      string   `json:"factor_type"`
	Species         string   `json:"species"`
	OnlyID          []string `json:"only_ID"`
	Tag             string   `json:"tag"`
	Email           string   `json:"email"`
}

// GoKeggPfam / GO/KEGG/pfam
/// python GFAP-linux.py -qp/qn 用户的输入文件或内容
//-aws 用户选择的内容
//-awd 用户选择的内容
//-go/kegg/pfam (这里是一个多选，根据用户选择，这里也会是-go -kegg -pfam)
//-am (fast 或者sensitive或者不设置该选项)
//-e 用户设置的值(可设可不设)
//-ap 用户设置的值(可设可不设)
//-only_ID (可设可不设)
//
//-o 保存的文件夹（如果前面的是一个多选，这里会同时产生多个结果文件，所以应该是一个文件夹的路径，然后将这个文件夹中的所有结果都发送给用户，发送完成后删除文件）

func GoKeggPfam(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py"

	if param.SequenceType != "" {
		command += " " + param.SequenceType
	}

	input := Utils.BaseDir + param.Tag
	/// 如果有输入的文本，则写入文件
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " " + input
	}
	if len(param.Species) != 0 {
		m := regexp.MustCompile("\\(\\w+\\)")
		species := m.ReplaceAllString(param.Species, "")
		command += " " + "-aws " + species
	}
	if len(param.Database) != 0 {
		command += " " + "-awd " + param.Database
	}
	if len(param.AnnotationType) != 0 {
		command += " " + strings.Join(param.AnnotationType, " ")
	}
	if len(param.AlignmentMode) != 0 {
		command += " " + "-am " + param.AlignmentMode
	}
	if len(param.EValue) != 0 {
		command += " " + "-e " + param.EValue
	}
	if len(param.MatchPercentage) != 0 {
		command += " " + "-ap " + param.MatchPercentage
	}
	if len(param.OnlyID) != 0 {
		command += " " + strings.Join(param.OnlyID, " ")
	}

	err := Utils.CmdExecutorSync(Utils.CmdParam{
		Tag:     param.Tag,
		Command: command,
		Input:   input,
		Email:   param.Email,
	})

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})
}

func MiRNAlncRNA(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -na"
	
	if len(param.InputType) != 0 {
		command += " " + "-nt " + param.InputType
	}
	input := Utils.BaseDir + param.Tag
	/// 如果有输入的文本，则写入文件
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " -qn " + input
	}
	if len(param.EValue) != 0 {
		command += " " + "-e " + param.EValue
	}

	err := Utils.CmdExecutorSync(Utils.CmdParam{
		Tag:     param.Tag,
		Command: command,
		Input:   input,
		Email:   param.Email,
	})
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})
}

func GeneFamilies(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py "

	input := Utils.BaseDir + param.Tag
	/// 如果有输入的文本，则写入文件
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.GeneSequence1 != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence1)
	}
	outputName := ""
	if param.SequenceType != "" {
		command += "-mf " + param.SequenceType
		outputName = "GFAP-families"
		if param.Tag != "" {
			command += " -qp " + input
		}
	} else {
		command += "-sf"
		outputName = "GFAP-single-family"
		if param.Tag != "" {
			command += " -qp " + input
		}
		if len(param.FactorType) != 0 {
			command += " " + "-mn " + param.FactorType
		}
	}
	err := Utils.CmdExecutorSync(Utils.CmdParam{
		Tag:        param.Tag,
		Command:    command,
		Input:      input,
		Email:      param.Email,
		OutputName: outputName,
	})
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})
}
