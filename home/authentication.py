import smtplib

def sendotp(receiver,otp):
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    email="com.theyouthblog@gmail.com"
    password="canttellyou"

    msg= "The one time password (OTP) to sign up at THE YOUTH BLOG is " +str(otp)
    server.login(email,password)
    server.sendmail(email,receiver,msg)

    server.quit()



