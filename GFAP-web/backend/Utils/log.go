package Utils

import (
	"github.com/gin-gonic/gin"
	"log"
	"os"
)

var (
	Debug   *log.Logger
	Info    *log.Logger
	Warning *log.Logger
	Error   *log.Logger
)

func InitLog() {
	// Logging to a file.
	logfile, _ := os.Create("gin.log")
	gin.DefaultWriter = logfile
	path, err := os.Getwd()
	if err != nil {
		log.Println(err)
	}
	BaseDir = path + "/com.gfap.upload/"
	OutputDir = path + "/com.gfap.output/"
	os.MkdirAll(BaseDir, 0755)
	os.MkdirAll(OutputDir, 0755)

	// set package-internal logger
	Info = log.New(logfile, "INFO: ", log.Ldate|log.Ltime)
	Warning = log.New(logfile, "WARN: ", log.Ldate|log.Ltime)
	Error = log.New(logfile, "ERROR: ", log.Ldate|log.Ltime)
}
