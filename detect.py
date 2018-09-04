#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import subprocess
import datetime
import smtplib

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
input_state = GPIO.input(27)

server_list = [#'192.168.1.11',
               #'192.168.1.12',
               #'192.168.1.13',
               '192.168.1.14',
               '192.168.1.15',
               '192.168.1.16',
               '192.168.1.17',
               '192.168.1.18',
               '192.168.1.21',
               '192.168.1.210',
               '192.168.1.211'
               ]


def send_mail():
    log_file = open('/var/log/power.log', 'r')
    log_msg = log_file.read()
    mail_srv = 'mail.novusgroup.co.za'
    mail_port = '25'
    mail_name = 'power@novusgroup.co.za'
    mail_recip = ['itmonitor@novusgroup.co.za']
    mail_sub = 'Power failure detected'
    mail_msg = 'Subject: {}\n\n{}'.format(mail_sub, log_msg)
    smtpServ = smtplib.SMTP(mail_srv, mail_port)
    smtpServ.sendmail(mail_name, mail_recip, mail_msg)
    log_file.close()
    smtpServ.quit()
    print('Sending email notification to: {}'.format(mail_recip))



print(timestamp, 'Running...')

while True:

    if input_state == 0:
        
        print(timestamp + ' Power outage detected')

        with open('/var/log/power.log', 'a') as f:
            f.write(timestamp + ' Power outage detected')
            f.write('\n')
            f.write(timestamp + ' Waiting 2 minutes to send shutdown signal')
            f.write('\n')
            time.sleep(120)
            input_state = GPIO.input(27)
            if input_state == False:
                f.write('Executing Shutdown...')
                for ip in server_list:
                    pass
                    subprocess.call('scp /root/shutdown.now root@{}:/root/'.format(ip), shell=True)
                send_mail()
                time.sleep(120)
