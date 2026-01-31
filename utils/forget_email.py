from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
import threading
User = get_user_model()


def send_password_reset_email(email, otp):
    
    def send():
        """
        Send password reset email to user
        """
        # subject = 'Reset Your PhiBook Password'
        html_message = f"""
        <html>
          <body style="background: #f4f6fb; font-family: 'Segoe UI', Arial, sans-serif; color: #222;">
            <div style="max-width: 480px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 24px rgba(85,128,193,0.10); overflow: hidden;">
              <div style="background: linear-gradient(90deg, #5580c1 60%, #3b5998 100%); padding: 24px 0;">
                <h2 style="color: #fff; text-align: center; font-size: 2rem; margin: 0; letter-spacing: 1px;">Password Reset Request</h2>
              </div>
              <div style="padding: 32px 28px 24px 28px;">
                <p style="font-size: 1.1rem; margin-bottom: 18px;">Hi <span style="color: #5580c1; font-weight: 600;">{email.split('@')[0]}</span>,</p>
                <p style="margin-bottom: 18px;">You requested a password reset for your <b>Sufi's Market</b> account. Here is your one-time password (OTP):</p>
                <div style="text-align: center; margin: 32px 0;">
                  <span style="display: inline-block; background: #eaf1fb; color: #2d3e50; font-size: 2.8em; font-weight: bold; letter-spacing: 8px; padding: 18px 36px; border-radius: 10px; border: 2px dashed #5580c1; box-shadow: 0 2px 8px rgba(85,128,193,0.08);">{otp}</span>
                </div>
                <p style="margin-bottom: 10px; color: #c0392b;"><b>Note:</b> The OTP will expire in <b>5 minutes</b>.</p>
                <p style="margin-bottom: 18px;">If you didn't request this, you can safely ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #e0e7ef; margin: 24px 0;">
                <p style="font-size: 1rem; color: #888;">Best regards,<br><span style="color: #5580c1;">The Sufis Team</span></p>
              </div>
            </div>
          </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        try:
            result = send_mail(
                subject="Reset Your PhiBook Password",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
            )
            print(f"send_mail returned: {result}")
            print("Email sent successfully")
            print(f"Sending password reset email...{email}")
            return True
        except Exception as e:
            import traceback
            print(f"Error sending email: {e}")
            traceback.print_exc()
            return False
    threading.Thread(target=send).start()



def send_mail_for_support(subject_, message, name, email):
    
    def send():
        """
        Send support email to admin
        """
        subject = subject_
        html_message = f"""
        <html>
          <body style="background: #f4f6fb; font-family: 'Segoe UI', Arial, sans-serif; color: #222;">
            <div style="max-width: 480px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 24px rgba(85,128,193,0.10); overflow: hidden;">
              
              <div style="padding: 28px 24px 20px 24px;">
                <p style="font-size: 1.1rem; margin-bottom: 16px;">Hi <span style="color: #5580c1; font-weight: 600;">Admin</span>,</p>
                <p style="margin-bottom: 16px;">You received a message from <b>{name}</b> email:(<a href="mailto:{email}" style="color:#3b5998;">{email}</a>).</p>
                <div style="text-align: center; margin: 28px 0;">
                  <span style="display: inline-block; background: #eaf1fb; color: #2d3e50; font-size: 1.2em; font-weight: 500; letter-spacing: 1px; padding: 16px 24px; border-radius: 10px; border: 2px dashed #5580c1; box-shadow: 0 2px 8px rgba(85,128,193,0.08);">{message}</span>
                </div>
                <hr style="border: none; border-top: 1px solid #e0e7ef; margin: 20px 0;">
                <p style="font-size: 1rem; color: #888;">Best regards,<br><span style="color: #5580c1;">The Sufis Team</span></p>
              </div>
            </div>
          </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                html_message=html_message,
            )
            print(f"Sending support email...{email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    threading.Thread(target=send).start()



def thanks_mail_for_getting_support(subject_,name,email):
    
    def send():
        """
        Send password reset email to user
        """
        subject = "Thank you for contacting Sufis Support"
        html_message = f"""
        <html>
          <body style="background: #f4f6fb; font-family: 'Segoe UI', Arial, sans-serif; color: #222;">
            <div style="max-width: 480px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 24px rgba(85,128,193,0.10); overflow: hidden;">
              
              <div style="padding: 28px 24px 20px 24px;">
                <p style="font-size: 1.1rem; margin-bottom: 16px;">Hi <span style="color: #5580c1; font-weight: 600;">{name}</span>,</p>
                <p style="margin-bottom: 16px;">We received your message successfully. Our dedicated team will get back to you shortly, Inshallah.</p>
                <div style="text-align: center; margin: 28px 0;">
                  <span style="display: inline-block; background: #eaf1fb; color: #2d3e50; font-size: 1.1em; font-weight: 500; letter-spacing: 1px; padding: 14px 22px; border-radius: 10px; border: 2px dashed #5580c1; box-shadow: 0 2px 8px rgba(85,128,193,0.08);">Your subject: {subject_}</span>
                </div>
                <hr style="border: none; border-top: 1px solid #e0e7ef; margin: 20px 0;">
                <p style="font-size: 1rem; color: #888;">Best regards,<br><span style="color: #5580c1;">The Sufis Team</span></p>
              </div>
            </div>
          </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
            )
            print(f"Sending support email...{email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    threading.Thread(target=send).start()