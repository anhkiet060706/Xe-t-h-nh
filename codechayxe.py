from machine import Pin, PWM, time_pulse_us
import time

ena = PWM(Pin(16), freq=1000)
in1 = Pin(15, Pin.OUT)
in2 = Pin(7, Pin.OUT)
enb = PWM(Pin(4), freq=1000)
in3 = Pin(6, Pin.OUT)
in4 = Pin(5, Pin.OUT)
trig = Pin(10, Pin.OUT)
echo = Pin(12, Pin.IN)
servo = PWM(Pin(3), freq=50)


SPEED_RUN = 720        
SPEED_TURN = 880       
STOP_DISTANCE = 10.0   
TURN_TIME = 0.45       

def set_servo_angle(angle):
    """Quay servo đến góc từ 0 đến 180 độ (0: Phải, 90: Giữa, 180: Trái)"""
    duty = int(1638 + (angle / 180.0) * (8192 - 1638))
    servo.duty_u16(duty)

def get_distance():
    """Đo khoảng cách bằng HC-SR04 và trả về đơn vị cm"""
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duration = time_pulse_us(echo, 1, 30000)
    
    if duration < 0:
        return 999.0  
        
    distance = (duration * 0.0343) / 2.0
    return round(distance, 1)

def set_speed(speed_a, speed_b):
    ena.duty(speed_a)
    enb.duty(speed_b)

def stop():
    set_speed(0, 0)
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

def move_forward():
    set_speed(SPEED_RUN, SPEED_RUN)
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def move_backward():
    set_speed(SPEED_RUN, SPEED_RUN)
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)

def turn_left():
    """Rẽ trái tại chỗ: Cụm A (Trái) lùi, Cụm B (Phải) tiến"""
    set_speed(SPEED_TURN, SPEED_TURN)
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)

def turn_right():
    """Rẽ phải tại chỗ: Cụm A (Trái) tiến, Cụm B (Phải) lùi"""
    set_speed(SPEED_TURN, SPEED_TURN)
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)

def main():
    print("KHỞI ĐỘNG HỆ THỐNG XE TỰ HÀNH")
    stop()
    set_servo_angle(90)  
    time.sleep(1)
    
    try:
        while True:
            dist_front = get_distance()
            print(f"[Đang quét phía trước] Khoảng cách: {dist_front} cm")
            
            if dist_front <= STOP_DISTANCE:
                stop()
                print(f"CẢNH BÁO: Phát hiện vật cản cách {dist_front} cm (<= {STOP_DISTANCE} cm) -> DỪNG XE!")
                time.sleep(0.3)
                
        
                set_servo_angle(170)
                time.sleep(0.5)  
                dist_left = get_distance()
                
              
                set_servo_angle(10)
                time.sleep(0.6)
                dist_right = get_distance()
                
                
                set_servo_angle(90)
                time.sleep(0.3)
                
                print(f"---> KẾT QUẢ ĐO 2 BÊN | Trái: {dist_left} cm | Phải: {dist_right} cm")
                
                
                if dist_left <= STOP_DISTANCE and dist_right <= STOP_DISTANCE:
                    print("===> Kẹt cả 2 bên! Lùi xe và xoay tìm đường mới")
                    move_backward()
                    time.sleep(0.4)
                    turn_left()
                    time.sleep(TURN_TIME * 1.5)
                    stop()
                elif dist_left > dist_right:
                    print(f"===> Bên TRÁI trống hơn ({dist_left} cm > {dist_right} cm) -> RẼ TRÁI!")
                    turn_left()
                    time.sleep(TURN_TIME)
                    stop()
                else:
                    print(f"===> Bên PHẢI trống hơn ({dist_right} cm >= {dist_left} cm) -> RẼ PHẢI!")
                    turn_right()
                    time.sleep(TURN_TIME)
                    stop()
                
                time.sleep(0.2)  
            else:
                
                move_forward()
                
            time.sleep(0.08)  
            
    except KeyboardInterrupt:
        stop()
        set_servo_angle(90)
        print("\n ĐÃ DỪNG XE AN TOÀN (Người dùng nhấn Stop/Ctrl+C) ")

if __name__ == "__main__":
    main()