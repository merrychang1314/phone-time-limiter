# -*- coding: utf-8 -*-
"""
手机时间限制器 - Android版本
功能：设定时间后进入只能拨打电话的模式
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os
import time
from datetime import datetime, timedelta

# 注册中文字体
try:
    # 尝试使用系统中文字体
    LabelBase.register(name="SimHei", 
                      fn_regular="DroidSansFallback.ttf")
except:
    # 如果没有找到字体文件，使用默认字体
    pass

class PhoneTimeLimiterApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limit_active = False
        self.end_time = None
        self.password = "1234"  # 默认密码
        
    def build(self):
        self.title = "手机时间限制器"
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title = Label(
            text='手机时间限制器',
            font_size='24sp',
            size_hint_y=None,
            height='60dp',
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title)
        
        # 状态显示
        self.status_label = Label(
            text='当前状态：未激活限制',
            font_size='16sp',
            size_hint_y=None,
            height='40dp'
        )
        main_layout.add_widget(self.status_label)
        
        # 时间设置区域
        time_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        time_layout.add_widget(Label(text='限制时长(分钟):', size_hint_x=0.4))
        
        self.time_input = TextInput(
            text='30',
            multiline=False,
            input_filter='int',
            size_hint_x=0.6
        )
        time_layout.add_widget(self.time_input)
        
        main_layout.add_widget(time_layout)
        
        # 密码设置区域
        password_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        password_layout.add_widget(Label(text='解锁密码:', size_hint_x=0.4))
        
        self.password_input = TextInput(
            text=self.password,
            multiline=False,
            password=True,
            size_hint_x=0.6
        )
        password_layout.add_widget(self.password_input)
        
        main_layout.add_widget(password_layout)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp', spacing=10)
        
        self.start_button = Button(
            text='开始限制',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.start_button.bind(on_press=self.start_limit)
        button_layout.add_widget(self.start_button)
        
        self.stop_button = Button(
            text='解除限制',
            background_color=(0.8, 0.2, 0.2, 1),
            disabled=True
        )
        self.stop_button.bind(on_press=self.show_password_popup)
        button_layout.add_widget(self.stop_button)
        
        main_layout.add_widget(button_layout)
        
        # 紧急呼叫按钮
        emergency_button = Button(
            text='紧急呼叫',
            background_color=(1, 0.5, 0, 1),
            size_hint_y=None,
            height='60dp'
        )
        emergency_button.bind(on_press=self.emergency_call)
        main_layout.add_widget(emergency_button)
        
        # 倒计时显示
        self.countdown_label = Label(
            text='',
            font_size='18sp',
            size_hint_y=None,
            height='40dp',
            color=(1, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.countdown_label)
        
        # 说明文字
        info_text = """
使用说明：
1. 设置限制时长（分钟）
2. 设置解锁密码
3. 点击"开始限制"激活
4. 限制期间只能拨打电话
5. 使用密码可提前解除限制
        """
        
        info_label = Label(
            text=info_text,
            font_size='12sp',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        main_layout.add_widget(info_label)
        
        return main_layout
    
    def start_limit(self, instance):
        """开始限制"""
        try:
            minutes = int(self.time_input.text)
            if minutes <= 0:
                self.show_message("错误", "请输入有效的时间（大于0的整数）")
                return
                
            # 更新密码
            self.password = self.password_input.text
            
            # 设置结束时间
            self.end_time = datetime.now() + timedelta(minutes=minutes)
            self.limit_active = True
            
            # 更新UI状态
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.time_input.disabled = True
            self.password_input.disabled = True
            
            self.status_label.text = f'限制已激活，将于 {self.end_time.strftime("%H:%M:%S")} 结束'
            
            # 开始倒计时
            Clock.schedule_interval(self.update_countdown, 1)
            
            # 在实际Android环境中，这里应该调用系统API来限制应用访问
            self.apply_restrictions()
            
        except ValueError:
            self.show_message("错误", "请输入有效的数字")
    
    def update_countdown(self, dt):
        """更新倒计时显示"""
        if not self.limit_active or not self.end_time:
            return False
            
        now = datetime.now()
        if now >= self.end_time:
            # 时间到，自动解除限制
            self.stop_limit_internal()
            return False
            
        remaining = self.end_time - now
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        self.countdown_label.text = f'剩余时间: {hours:02d}:{minutes:02d}:{seconds:02d}'
        return True
    
    def show_password_popup(self, instance):
        """显示密码输入弹窗"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(text='请输入解锁密码:', size_hint_y=None, height='40dp'))
        
        password_input = TextInput(
            multiline=False,
            password=True,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(password_input)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)
        
        confirm_btn = Button(text='确认')
        cancel_btn = Button(text='取消')
        
        button_layout.add_widget(confirm_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='解锁验证',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        def check_password(instance):
            if password_input.text == self.password:
                popup.dismiss()
                self.stop_limit_internal()
            else:
                self.show_message("错误", "密码错误！")
        
        def cancel(instance):
            popup.dismiss()
        
        confirm_btn.bind(on_press=check_password)
        cancel_btn.bind(on_press=cancel)
        
        popup.open()
    
    def stop_limit_internal(self):
        """内部解除限制方法"""
        self.limit_active = False
        self.end_time = None
        
        # 更新UI状态
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.time_input.disabled = False
        self.password_input.disabled = False
        
        self.status_label.text = '当前状态：未激活限制'
        self.countdown_label.text = ''
        
        # 解除系统限制
        self.remove_restrictions()
        
        Clock.unschedule(self.update_countdown)
    
    def emergency_call(self, instance):
        """紧急呼叫功能"""
        try:
            # 在Android环境中调用拨号器
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse("tel:110"))  # 紧急电话号码
            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(intent)
            
        except ImportError:
            # 桌面环境下的模拟
            self.show_message("紧急呼叫", "在真实Android环境中将拨打紧急电话")
    
    def apply_restrictions(self):
        """应用系统限制（需要Android权限）"""
        try:
            # 这里应该实现实际的应用限制逻辑
            # 在真实的Android环境中，需要：
            # 1. 获取设备管理员权限
            # 2. 使用DevicePolicyManager限制应用
            # 3. 或者使用AccessibilityService监控应用启动
            pass
        except Exception as e:
            print(f"应用限制失败: {e}")
    
    def remove_restrictions(self):
        """移除系统限制"""
        try:
            # 移除之前应用的限制
            pass
        except Exception as e:
            print(f"移除限制失败: {e}")
    
    def show_message(self, title, message):
        """显示消息弹窗"""
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='确定', size_hint_y=None, height='40dp')
        content.add_widget(btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    PhoneTimeLimiterApp().run()