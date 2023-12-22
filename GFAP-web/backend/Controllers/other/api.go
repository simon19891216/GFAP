package other

import (
	"backend/Utils"
	"github.com/gin-gonic/gin"
	"net/http"
	// "strings"
)

type Body struct {
	AnnotationType []string `json:"annotation_type"`
	CutValue       string   `json:"cut_value"`
	GeneNumber     string   `json:"gene_number"`
	GeneID         string   `json:"geneid"`
	GOID           string   `json:"goid"`
	PValue         string   `json:"pValue"`
	ThresholdValue string   `json:"threshold_value"`
	DrawTypes      string   `json:"draw_type"`
	ColorModel     string   `json:"colormodel"`
	Color          string   `json:"color"`
	SingleColor    []string `json:"singlecolor"`
	GeneSequence   string   `json:"gene_sequence"`
	CodeSequence   string   `json:"code_sequence"`
	InputType      string   `json:"input_type"`
	SequenceType   string   `json:"sequence_type"`
	FactorType     string   `json:"factor_type"`
	SaveType       string   `json:"save_type"`
	Species        string   `json:"species"`
	GoCategory     string   `json:"go_category"`
	OnlyID         []string `json:"only_ID"`
	Tag            string   `json:"tag"`
	Tag1           string   `json:"tag1"`
	Tag2           string   `json:"tag2"`
	DirTag         string   `json:"dir_tag"`
	Email          string   `json:"email"`
}

func Translation(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -t"

	input := Utils.BaseDir + param.Tag
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " -qn " + input
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

func RNA2DNA(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -rd"

	input := Utils.BaseDir + param.Tag
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " -qn " + input
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

func Extraction(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -ex"

	input := Utils.BaseDir + param.Tag
	if param.Tag != "" {
		command += " -ar " + input
	}
	input1 := Utils.BaseDir + param.Tag1
	if param.Tag1 != "" {
		command += " -ID " + input1
	}
	if param.SequenceType != "" {
		command += " " + param.SequenceType
	}

	err := Utils.CmdExecutorSync2Input(Utils.CmdParam{
		Tag:     param.Tag,
		Command: command,
		Input:   input,
		Email:   param.Email,
	}, input1)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})
}

func Merge(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -mr"

	input := Utils.BaseDir + param.Tag
	if param.Tag != "" {
		command += " -qn " + input
	}
	Dir := Utils.BaseDir + param.DirTag
	if param.Tag != "" {
		command += " -rp " + Dir
	}

	err := Utils.CmdExecutorSync2Input(Utils.CmdParam{
		Tag:     param.Tag,
		Command: command,
		Input:   input,
		Email:   param.Email,
	}, Dir)

	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"command": command, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"command": command, "url": Utils.Cfg.Host + param.Tag + ".zip"})
}

func ExtractCode(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py"

	input := Utils.BaseDir + param.Tag
	if param.CodeSequence != "" {
		Utils.GenerateFileFromInput(input, param.CodeSequence)
	}
	if param.Tag != "" {
		command += " -qn " + input
	}
	command += " -plt"

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

func BuildDatabase(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -bsd"

	input := Utils.BaseDir + param.Tag
	if param.CodeSequence != "" {
		Utils.GenerateFileFromInput(input, param.CodeSequence)
	}
	if param.Tag != "" {
		command += " -qn " + input
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

func Conversion(c *gin.Context) {
	var param Body
	if err := c.ShouldBindJSON(&param); err != nil {
		Utils.Error.Println(err)
	}
	command := "python GFAP-linux.py -cf"

	input := Utils.BaseDir + param.Tag
	if param.GeneSequence != "" {
		Utils.GenerateFileFromInput(input, param.GeneSequence)
	}
	if param.Tag != "" {
		command += " -gf " + input
	}
	if len(param.GeneID) != 0 {
		command += " " + "-gid " + param.GeneID
	}
	if len(param.GOID) != 0 {
		command += " " + "-fid " + param.GOID
	}
	if len(param.PValue) != 0 {
		command += " " + "-pvalue_index " + param.PValue
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
