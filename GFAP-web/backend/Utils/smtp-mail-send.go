package Utils

import (
	mail "github.com/xhit/go-simple-mail/v2"
)

var htmlBody = `
<html>
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <title>This email is automatically sent by GFAP, do not reply</title>
</head>
<body>
   <p>annotation results</p>
</body> `

func SendEmail(attachments []string, to string, error string) bool {
	if Cfg.Debug == true {
		return true
	}
	from := Cfg.EmailUser
	pass := Cfg.EmailPwd
	server := mail.NewSMTPClient()
	server.Host = Cfg.EmailHost
	server.Port = Cfg.EmailPort
	server.Username = from
	server.Password = pass
	server.Encryption = mail.EncryptionSSL

	smtpClient, err := server.Connect()
	if err != nil {
		Error.Println(err)
	}

	// Create email
	email := mail.NewMSG()
	email.SetFrom("<" + from + ">")
	email.SetSubject("This email is automatically sent by GFAP, do not reply")
	email.AddTo(to)
	if error != "" {
		email.SetBody(mail.TextPlain, error)
	} else {
		email.SetBody(mail.TextHTML, htmlBody)
	}

	for _, attachment := range attachments {
		email.AddAttachment(attachment)
	}
	// Send email
	err = email.Send(smtpClient)
	if err != nil {
		Error.Println(err)
	}
	return err != nil
}
