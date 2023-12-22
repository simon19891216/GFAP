package main

import (
	"backend/Router"
	"backend/Utils"
	"flag"
	"fmt"
	"github.com/ilyakaznacheev/cleanenv"
	"os"
)

// Args command-line parameters
type Args struct {
	ConfigPath string
}

func main() {
	Utils.InitLog()
	Utils.Info.Println("InitLog")
	args := ProcessArgs(&Utils.Cfg)
	Utils.Info.Println("ProcessArgs : " + args.ConfigPath)
	Utils.Info.Println(args.ConfigPath)
	if err := Utils.LoadConfig(args.ConfigPath); err != nil {
		Utils.Info.Println(err)
	}
	Router.InitRouter()
}

// ProcessArgs processes and handles CLI arguments
func ProcessArgs(cfg interface{}) Args {
	var a Args

	f := flag.NewFlagSet("Example server", 1)
	f.StringVar(&a.ConfigPath, "c", "config.yml", "Path to configuration file")

	fu := f.Usage
	f.Usage = func() {
		fu()
		envHelp, _ := cleanenv.GetDescription(cfg, nil)
		fmt.Fprintln(f.Output())
		fmt.Fprintln(f.Output(), envHelp)
	}

	f.Parse(os.Args[1:])
	return a
}
