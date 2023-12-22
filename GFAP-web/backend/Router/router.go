package Router

import (
	"backend/Controllers/annotation"
	"backend/Controllers/draw"
	"backend/Controllers/other"
	"backend/Controllers/upload"
	"backend/Middlewares"
	"github.com/gin-gonic/gin"
)

func InitRouter() {
	gin.DisableConsoleColor()
	gin.SetMode(gin.ReleaseMode)
	router := gin.Default()
	router.Use(gin.Recovery())
	router.Use(Middlewares.Cors()) //开启中间件 允许使用跨域请求
	router.POST("/api/upload", upload.ToFile)
	router.POST("/api/uploadDir", upload.ToDir)
	router.POST("/api/go_kegg_pfam", annotation.GoKeggPfam)
	router.POST("/api/miRNA_lncRNA", annotation.MiRNAlncRNA)
	router.POST("/api/gene_families", annotation.GeneFamilies)
	router.POST("/api/statistics", draw.Statistics)
	router.POST("/api/pathway", draw.PathWay)
	router.POST("/api/translation", other.Translation)
	router.POST("/api/RNA2DNA", other.RNA2DNA)
	router.POST("/api/extraction", other.Extraction)
	router.POST("/api/merge", other.Merge)
	router.POST("/api/extractcode",other.ExtractCode)
	router.POST("/api/conversion", other.Conversion)
	router.POST("/api/builddatabase",other.BuildDatabase)
	router.Run(":10001")
}
