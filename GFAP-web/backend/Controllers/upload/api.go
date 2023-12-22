package upload

import (
	"backend/Utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
)

// ToFile 上传文件
func ToFile(c *gin.Context) {
	_, headers, err := c.Request.FormFile("file")
	if err != nil {
		c.String(500, "Error when try to get file: %v", err)
	}
	tag := c.DefaultQuery("tag", "-1")
	target := Utils.BaseDir + tag
	err = c.SaveUploadedFile(headers, target)
	if err != nil {
		Utils.Error.Println(err.Error())
		return
	}
	Utils.Info.Println("upload file with tag " + tag)
	c.String(http.StatusOK, tag)
}

func ToDir(c *gin.Context) {
	_, headers, err := c.Request.FormFile("file")
	if err != nil {
		c.String(500, "Error when try to get file: %v", err)
	}
	tag := c.DefaultQuery("tag", "-1")
	dir := c.DefaultQuery("dir", "-1")

	os.MkdirAll(Utils.BaseDir+dir+"/", 0755)
	target := Utils.BaseDir + dir + "/" + tag
	err = c.SaveUploadedFile(headers, target)
	if err != nil {
		Utils.Error.Println(err.Error())
		return
	}
	Utils.Info.Println("upload file with tag " + tag)
	c.String(http.StatusOK, tag)
}
