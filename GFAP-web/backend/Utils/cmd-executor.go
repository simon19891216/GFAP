package Utils

import (
	"archive/zip"
	"bufio"
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
)

type CmdParam struct {
	Tag        string
	Command    string
	Input      string
	Email      string
	OutputName string
}

func GenerateFileFromInput(filePath string, geneSequence string) {
	_ = os.Remove(filePath)
	file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		Info.Println("GenerateFileFromInput OpenFile :" + err.Error())
	}
	_, _ = file.WriteString(geneSequence)
	if err != nil {
		Info.Println("GenerateFileFromInput : WriteString " + err.Error())
	}
	_ = file.Close()
}

func CmdExecutor(param CmdParam) func() {
	return func() {
		/// 创建本次任务的临时输出文件夹
		command := param.Command
		input := param.Input
		email := param.Email
		array := strings.Split(input, "/")
		fileName := array[len(array)-1]
		output := OutputDir + fileName + "/"
		os.MkdirAll(output, 0755)
		command = Cfg.PythonHome + command + " -o " + output
		if param.OutputName != "" {
			command = command + param.OutputName + ".txt"
		}
		Info.Println("开始异步执行:" + command)

		err := execute(command)

		// 清理本次任务的临时输出文件夹
		defer os.RemoveAll(output)
		defer os.Remove(input)
		// if err != nil {
		// 	if email != "" {
		// 		SendEmail(nil, email, err.Error())
		// 	}
		// 	return err
		// }
		if err != nil {
			SendEmail(nil, email, err.Error())
			return
		}

		if _, err := os.Stat(input + ".index"); err == nil {
			fmt.Printf(".index file exists")
			err := os.Rename(input+".index", output+param.OutputName+".index")
			if err != nil {
				Info.Println(err)
			}
		}
		/// 遍历本次任务的输出文件夹中所有文件，
		files, err := ioutil.ReadDir(output)
		if err != nil {
			Info.Println(err)
		}
		var attachments []string
		for _, file := range files {
			attachments = append(attachments, output+file.Name())
		}
		/// 发送邮件
		if email != "" {
			var attachments []string
			for _, file := range files {
				attachments = append(attachments, output+file.Name())
			}
			/// 发送邮件
			SendEmail(attachments, email, "")
		} else {
			archiveOutputToZipFile(param, output)
		}
		// SendEmail(attachments, email, "")
		Info.Println("同步执行完成")
	}
}

func CmdExecutorSync(param CmdParam) (errRsp error) {
	/// 创建本次任务的临时输出文件夹
	command := param.Command
	input := param.Input
	email := param.Email
	array := strings.Split(input, "/")
	fileName := array[len(array)-1]
	output := OutputDir + fileName + "/"
	os.RemoveAll(output)
	os.MkdirAll(output, 0755)
	command = Cfg.PythonHome + command + " -o " + output

	Info.Println("开始同步执行:" + command)

	err := execute(command)

	// 清理本次任务的临时输出文件夹
	defer os.RemoveAll(output)
	defer os.Remove(input)

	if err != nil {
		if email != "" {
			SendEmail(nil, email, err.Error())
		}
		Info.Println("同步执行错误:" + err.Error())
		return err
	}

	if _, err := os.Stat(input + ".index"); err == nil {
		fmt.Printf(".index file exists")
		err := os.Rename(input+".index", output+param.OutputName+".index")
		if err != nil {
			Info.Println(err)
		}
	}
	/// 遍历本次任务的输出文件夹中所有文件，
	files, err := ioutil.ReadDir(output)
	if err != nil {
		Info.Println(err)
	}
	for _, file := range files {
		Info.Println("同步执行产生结果: ", output+file.Name())
		if strings.Contains(file.Name(), "error") {
			Info.Println("同步执行产生错误文件 : ", output+file.Name())
			errorMsg, _ := ioutil.ReadFile(output + file.Name())
			return errors.New(string(errorMsg))
		}
	}
	if email != "" {
		var attachments []string
		for _, file := range files {
			attachments = append(attachments, output+file.Name())
		}
		/// 发送邮件
		SendEmail(attachments, email, "")
	} else {
		archiveOutputToZipFile(param, output)
	}
	if param.OutputName != "" {
		if _, err := os.Stat(output + param.OutputName); err == nil {
			Info.Println(param.OutputName + " file exists")
			err := os.Rename(output+param.OutputName, Cfg.DrawDir+fileName+".svg")
			if err != nil {
				Info.Println("failed to move svg file with error:" + err.Error())
			} else {
				Info.Println("success to move " + output + param.OutputName + " to " + Cfg.DrawDir + fileName + ".svg")
			}
		}
	}
	Info.Println("同步执行完成")
	return nil
}

func archiveOutputToZipFile(param CmdParam, output string) {
	//Info.Println("param.Input: " + param.Input)
	//Info.Println("output: " + output)
	//err := os.Rename(param.Input, output+param.Tag)
	//if err != nil {
	//	Info.Println(err)
	//}
	zipPath := Cfg.DrawDir + param.Tag + ".zip"
	Info.Println("creating zip archive...")
	archive, err := os.Create(zipPath)
	if err != nil {
		Info.Println(err)
	}
	zipWriter := zip.NewWriter(archive)
	files, err := ioutil.ReadDir(output)
	if err != nil {
		Info.Println(err)
	}
	for _, file := range files {
		Info.Println("opening file ", output+file.Name())
		f1, err := os.Open(output + file.Name())
		if err != nil {
			Info.Println(err)
		}

		Info.Println("writing ", file.Name())
		w1, err := zipWriter.Create("result/" + file.Name())
		if err != nil {
			Info.Println(err)
		}
		written, err := io.Copy(w1, f1)
		if err != nil {
			Info.Println(err)
		}
		Info.Println("written", strconv.FormatInt(written, 10))
		f1.Close()
	}
	zipWriter.Close()
	archive.Close()
}

func CmdExecutorSync2Input(param CmdParam, dir string) (errRsp error) {

	command := param.Command
	input := param.Input
	email := param.Email
	/// 创建本次任务的临时输出文件夹
	array := strings.Split(input, "/")
	fileName := array[len(array)-1]
	output := OutputDir + fileName + "/"
	os.RemoveAll(output)
	os.MkdirAll(output, 0755)
	command = Cfg.PythonHome + command + " -o " + output
	Info.Println("开始异步执行:" + command)

	err := execute(command)

	// 清理本次任务的临时输出文件夹
	defer os.RemoveAll(output)
	defer os.Remove(input)
	if dir != BaseDir {
		defer os.RemoveAll(dir)
		defer os.Remove(dir)
	}

	if err != nil {
		SendEmail(nil, email, err.Error())
		return
	}
	// if err != nil {
	// 	if email != "" {
	// 		SendEmail(nil, email, err.Error())
	// 	}
	// 	return err
	// }

	/// 遍历本次任务的输出文件夹中所有文件，
	files, err := ioutil.ReadDir(output)
	if err != nil {
		Info.Println(err)
	}
	var attachments []string
	for _, file := range files {
		attachments = append(attachments, output+file.Name())
		Info.Println("同步执行产生结果: ", output+file.Name())
		if strings.Contains(file.Name(), "error") {
			Info.Println("同步执行产生错误文件 : ", output+file.Name())
			errorMsg, _ := ioutil.ReadFile(output + file.Name())
			return errors.New(string(errorMsg))
		}
	}

	/// 发送邮件
	if email != "" {
		var attachments []string
		for _, file := range files {
			attachments = append(attachments, output+file.Name())
		}
		/// 发送邮件
		SendEmail(attachments, email, "")
	} else {
		archiveOutputToZipFile(param, output)
	}
	// SendEmail(attachments, email, "")
	Info.Println("同步执行完成")
	return nil
}

func execute(cmd string) (err error) {
	if cmd == "" {
		return errors.New("no command provided")
	}

	cmdArr := strings.Split(cmd, " ")
	name := cmdArr[0]

	var args []string
	if len(cmdArr) > 1 {
		args = cmdArr[1:]
	}

	command := exec.Command(name, args...)
	command.Env = os.Environ()

	stdout, err := command.StdoutPipe()
	if err != nil {
		Error.Println("Failed creating command stdout pipe: ", err)
		return err
	}
	defer stdout.Close()
	stdoutReader := bufio.NewReader(stdout)

	stderr, err := command.StderrPipe()
	if err != nil {
		Error.Println("Failed creating command std err pipe: ", err)
		return err
	}
	defer stderr.Close()
	stderrReader := bufio.NewReader(stderr)

	if err := command.Start(); err != nil {
		Error.Println("Failed starting command: ", err)
		return err
	}

	go handleReader(stdoutReader)
	go handleReader(stderrReader)

	if err := command.Wait(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			if status, ok := exitErr.Sys().(syscall.WaitStatus); ok {
				Info.Println("Exit Status: ", status.ExitStatus())
				if status.ExitStatus() == 1 {
					return errors.New("please input the content in the correct format")
				}
				return err
			}
		}
		return err
	}
	return nil
}

func handleReader(reader *bufio.Reader) {
	for {
		str, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		str = strings.TrimSuffix(str, "\n")
		Info.Println(str)
	}
}
