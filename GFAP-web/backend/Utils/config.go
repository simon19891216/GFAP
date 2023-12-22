package Utils

import (
	"github.com/ilyakaznacheev/cleanenv"
)

var BaseDir = ""
var OutputDir = ""
var Cfg Config

type Config struct {
	PythonHome string `yaml:"PythonHome" env:"PythonHome"`
	EmailUser  string `yaml:"EmailUser" env:"EmailUser"`
	EmailPwd   string `yaml:"EmailPwd" env:"EmailPwd"`
	EmailHost  string `yaml:"EmailHost" env:"EmailHost"`
	EmailPort  int    `yaml:"EmailPort" env:"EmailPort"`
	DrawDir    string `yaml:"DrawDir" env:"DrawDir"`
	Host       string `yaml:"Host" env:"Host"`
	Debug      bool   `yaml:"Debug" env:"Debug"`
}

func LoadConfig(path string) error {
	err := cleanenv.ReadConfig(path, &Cfg)
	if err != nil {
		Error.Fatal("Failed to read config")
		return err
	}
	Info.Println("succeeded to read config")
	return nil
}
