package draw

import (
	"backend/Utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"regexp"
	"strings"
)

type Body struct {
	AlignmentMode  string   `json:"alignment_mode"`
	AnnotationType string 	`json:"annotation_type"`
	Database       string   `json:"database"`
	CutValue       string   `json:"cut_value"`
	GeneNumber     string   `json:"gene_number"`
	PValue         string   `json:"pvalue"`
	ThresholdValue string   `json:"threshold_value"`
	DrawTypes      string   `json:"draw_type"`
	ColorModel     string   `json:"colormodel"`
	Color          string   `json:"color"`
	SingleColor    []string `json:"singlecolor"`
	GeneSequence   string   `json:"gene_sequence"`
	InputType      string   `json:"input_type"`
	SequenceType   string   `json:"sequence_type"`
	FactorType     string   `json:"factor_type"`
	SaveType       string   `json:"save_type"`
	Species        string   `json:"species"`
	GoCategory     string   `json:"go_category"`
	OnlyID         []string `json:"only_ID"`
	Tag            string   `json:"tag"`
	Email          string   `json:"email"`
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

func Statistics(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -ds"

	input := Utils.BaseDir + param.Tag
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " -ar " + input
	}
	if len(param.CutValue) != 0 {
		command += " " + "-cut_value " + param.CutValue
	}
	if len(param.GeneNumber) != 0 {
		command += " " + "-gn " + param.GeneNumber
	}
	if len(param.DrawTypes) != 0 {
		command += " " + "-drawtypes " + param.DrawTypes
	}
	if len(param.ColorModel) != 0 {
		command += " " + "-colormodel " + param.ColorModel
	}
	if len(param.Color) != 0 {
		command += " " + "-color " + param.Color
	}
	if len(param.SingleColor) != 0 {
		command += " " + strings.Join(param.SingleColor, " ")
	}
	if len(param.SaveType) != 0 {
		command += " " + "-st " + param.SaveType
	}
	if len(param.AnnotationType) != 0 {
		// command += " " + strings.Join(param.AnnotationType, " ")
		command += " " + param.AnnotationType
	}

	err := Utils.CmdExecutorSync(Utils.CmdParam{
		Tag:        param.Tag,
		Command:    command,
		Input:      input,
		Email:      param.Email,
		OutputName: "draw_detail." + param.SaveType,
	})
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})
}

func PathWay(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -dn"

	input := Utils.BaseDir + param.Tag
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " -ar " + input
	}
	if len(param.CutValue) != 0 {
		command += " " + "-cut_value " + param.CutValue
	}
	if len(param.GeneNumber) != 0 {
		command += " " + "-gn " + param.GeneNumber
	}
	if len(param.PValue) != 0 {
		command += " " + "-pvalue " + param.PValue
	}
	if len(param.ColorModel) != 0 {
		command += " " + "-colormodel " + param.ColorModel
	}
	if len(param.Species) != 0 {
		m := regexp.MustCompile("\\(\\w+\\)")
		species := m.ReplaceAllString(param.Species, "")
		command += " " + "-aws " + species
	}
	if len(param.ThresholdValue) != 0 {
		command += " " + "-ap " + param.ThresholdValue
	}
	if len(param.SaveType) != 0 {
		command += " " + "-st " + param.SaveType
	}
	if len(param.GoCategory) != 0 {
		command += " " + "-gca " + param.GoCategory
	}
	if len(param.AnnotationType) != 0 {
		// command += " " + strings.Join(param.AnnotationType, " ")
		command += " " + param.AnnotationType
	}

	err := Utils.CmdExecutorSync(Utils.CmdParam{
		Tag:        param.Tag,
		Command:    command,
		Input:      input,
		Email:      param.Email,
		OutputName: "draw_detail." + param.SaveType,
	})
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})

}
