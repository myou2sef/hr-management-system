from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from zk import ZK, const
from .models import ZKDevice, AttendanceLog
from datetime import datetime
import json
import socket
import time

def try_connection(ip, port):
    """محاولة الاتصال بالجهاز باستخدام إعدادات مختلفة"""
    errors = []
    
    # قائمة بمختلف إعدادات الاتصال للتجربة
    configs = [
        {'force_udp': True, 'ommit_ping': True},
        {'force_udp': False, 'ommit_ping': True},
        {'force_udp': True, 'ommit_ping': False},
        {'force_udp': False, 'ommit_ping': False}
    ]
    
    for config in configs:
        try:
            print(f"محاولة الاتصال باستخدام الإعدادات: {config}")
            zk = ZK(ip, port=port, timeout=5, password=0, **config)
            conn = zk.connect()
            if conn:
                return conn, None
        except Exception as e:
            errors.append(f"فشل الاتصال مع {config}: {str(e)}")
            time.sleep(1)  # انتظار قليلاً قبل المحاولة التالية
    
    return None, errors

@csrf_exempt
def fetch_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ip = data.get('ip')
            port = data.get('port', 4370)
            
            print(f"محاولة الاتصال بـ IP: {ip}, Port: {port}")
            
            # التحقق من صحة عنوان IP
            try:
                socket.inet_aton(ip)
            except socket.error:
                print("عنوان IP غير صالح")
                return JsonResponse({
                    'status': 'error',
                    'message': 'عنوان IP غير صالح'
                }, status=400)
            
            # محاولة الاتصال بالجهاز
            conn, errors = try_connection(ip, port)
            
            if conn:
                try:
                    print("تم الاتصال بنجاح")
                    print("جاري قراءة سجلات الحضور...")
                    attendance = conn.get_attendance()
                    print(f"تم استلام {len(attendance) if attendance else 0} سجل")
                    
                    if not attendance:
                        print("لا توجد سجلات حضور")
                        return JsonResponse({
                            'status': 'success',
                            'data': []
                        })
                    
                    attendance_data = []
                    for record in attendance:
                        print(f"معالجة سجل: User ID: {record.user_id}, Time: {record.timestamp}")
                        attendance_data.append({
                            'user_id': record.user_id,
                            'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            'status': record.status,
                            'punch': record.punch
                        })
                    
                    print(f"تم معالجة {len(attendance_data)} سجل بنجاح")
                    return JsonResponse({
                        'status': 'success',
                        'data': attendance_data
                    })
                    
                except Exception as e:
                    error_message = str(e)
                    print(f"خطأ في قراءة البيانات: {error_message}")
                    print(f"نوع الخطأ: {type(e).__name__}")
                    return JsonResponse({
                        'status': 'error',
                        'message': f'خطأ في قراءة البيانات: {error_message}'
                    }, status=500)
                    
                finally:
                    try:
                        conn.disconnect()
                        print("تم قطع الاتصال بنجاح")
                    except Exception as e:
                        print(f"خطأ في قطع الاتصال: {str(e)}")
            else:
                error_message = "\n".join(errors)
                print(f"فشلت جميع محاولات الاتصال: {error_message}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'فشل الاتصال بالجهاز. تفاصيل الأخطاء:\n{error_message}'
                }, status=500)
                
        except json.JSONDecodeError as e:
            print(f"خطأ في تحليل البيانات JSON: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'بيانات غير صالحة'
            }, status=400)
        except Exception as e:
            print(f"خطأ غير متوقع: {str(e)}")
            print(f"نوع الخطأ: {type(e).__name__}")
            return JsonResponse({
                'status': 'error',
                'message': f'خطأ غير متوقع: {str(e)}'
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'طريقة غير مسموحة'
    }, status=405)

def home(request):
    devices = ZKDevice.objects.all()
    return render(request, 'attendance/home.html', {'devices': devices})
